import tkinter as tk
from PIL import Image, ImageTk
import numpy as np

class PanZoomCanvas(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pil_image = None  # Image data to be displayed
        self.original_image = None  # Store the original image
        self.original_width = None
        self.original_height = None

        self.zoom_cycle = 0
        self.__old_event = None  # Initialize __old_event

        self.create_widget()  # Create canvas

        # Initial affine transformation matrix
        self.reset_transform()

    # Define the create_widget method.
    def create_widget(self):
        # Canvas
        self.canvas = tk.Canvas(self, background="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Controls
        self.canvas.bind("<Button-1>", self.mouse_down_left)  # MouseDown
        self.canvas.bind("<B1-Motion>", self.mouse_move_left)  # MouseDrag
        self.canvas.bind("<MouseWheel>", self.mouse_wheel)  # MouseWheel
        self.canvas.bind("<Button-2>", self.mouse_down_middle)  # MouseWheel ButtonDown
        self.canvas.bind("<B2-Motion>", self.mouse_move_middle)  # MouseWheel ButtonDrag

    def set_image(self, filename):
        '''To open an image file'''
        if not filename:
            return
        # PIL.Image
        self.original_image = Image.open(filename)
        self.pil_image = self.original_image.copy()
        self.original_width, self.original_height = self.pil_image.size
        # Set the affine transformation matrix to display the entire image.
        self.reset_transform()
        # Adjust canvas size based on image dimensions
        self.canvas.config(scrollregion=(0, 0, self.original_width, self.original_height))
        self.canvas.config(width=self.original_width, height=self.original_height)
        # To display the image
        self.draw_image(self.pil_image)

    # -------------------------------------------------------------------------------
    # Mouse events
    # -------------------------------------------------------------------------------
    def mouse_down_left(self, event):
        self.__old_event = event

    def mouse_move_left(self, event):
        if self.pil_image is None:
            return

        if self.__old_event is None:
            self.__old_event = event
            return

        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event

    def mouse_down_middle(self, event):
        self.__old_event = event

    def mouse_move_middle(self, event):
        if self.pil_image is None:
            return

        if self.__old_event is None:
            self.__old_event = event
            return

        self.translate(event.x - self.__old_event.x, event.y - self.__old_event.y)
        self.redraw_image()
        self.__old_event = event

    def mouse_wheel(self, event):
        if self.pil_image is None:
            return

        if event.delta < 0:
            self.zoom_out(event.x, event.y)
        else:
            self.zoom_in(event.x, event.y)

    # -------------------------------------------------------------------------------
    # Zoom functions
    # -------------------------------------------------------------------------------
    def zoom_in(self, cx=None, cy=None):
        if self.pil_image is None or self.zoom_cycle >= 20:
            return
        if cx is None or cy is None:
            cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.scale_at(1.25, cx, cy)
        self.zoom_cycle += 1
        self.redraw_image()

    def zoom_out(self, cx=None, cy=None):
        if self.pil_image is None or self.zoom_cycle <= 0:
            return
        if cx is None or cy is None:
            cx, cy = self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2
        self.scale_at(0.8, cx, cy)
        self.zoom_cycle -= 1
        self.redraw_image()

    # -------------------------------------------------------------------------------
    # Affine Transformation for Image Display
    # -------------------------------------------------------------------------------
    def reset_transform(self):
        self.mat_affine = np.eye(3)  # 3x3 identity matrix

    def translate(self, offset_x, offset_y, zoom=False):
        mat = np.eye(3)  # 3x3 identity matrix
        mat[0, 2] = float(offset_x)
        mat[1, 2] = float(offset_y)
        new_mat_affine = np.dot(mat, self.mat_affine)

        # Calculate the new top-left and bottom-right corners of the image
        top_left = np.dot(new_mat_affine, [0, 0, 1])
        bottom_right = np.dot(new_mat_affine, [self.original_width, self.original_height, 1])

        # Limit the translation to prevent the image from moving outside its bounds
        if top_left[0] > 0:
            new_mat_affine[0, 2] -= top_left[0]
        if top_left[1] > 0:
            new_mat_affine[1, 2] -= top_left[1]
        if bottom_right[0] < self.canvas.winfo_width():
            new_mat_affine[0, 2] += self.canvas.winfo_width() - bottom_right[0]
        if bottom_right[1] < self.canvas.winfo_height():
            new_mat_affine[1, 2] += self.canvas.winfo_height() - bottom_right[1]

        self.mat_affine = new_mat_affine

    def scale(self, scale: float):
        mat = np.eye(3)  # 3x3 identity matrix
        mat[0, 0] = scale
        mat[1, 1] = scale
        self.mat_affine = np.dot(mat, self.mat_affine)

    def scale_at(self, scale: float, cx: float, cy: float):
        # Translate to the origin
        self.translate(-cx, -cy, True)
        # Scale
        self.scale(scale)
        # Restore
        self.translate(cx, cy)

    def to_image_point(self, x, y):
        '''Convert coordinates from the canvas to the image'''
        if self.pil_image is None:
            return []
        # Convert coordinates from the canvas to the image by taking the inverse of the transformation matrix.
        mat_inv = np.linalg.inv(self.mat_affine)
        image_point = np.dot(mat_inv, [x, y, 1.])
        if image_point[0] < 0 or image_point[1] < 0 or image_point[0] > self.original_width or image_point[1] > self.original_height:
            return []
        return image_point[:2]

    def to_canvas_point(self, x, y):
        '''Convert coordinates from the image to the canvas'''
        if self.pil_image is None:
            return []
        # Convert coordinates from the image to the canvas using the transformation matrix.
        canvas_point = np.dot(self.mat_affine, [x, y, 1.])
        return canvas_point[:2]

    # -------------------------------------------------------------------------------
    # Drawing
    # -------------------------------------------------------------------------------
    def draw_image(self, pil_image):
        if pil_image is None:
            return

        self.pil_image = pil_image

        # Canvas size
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # Calculate the affine transformation matrix from canvas to image data
        # (Calculate the inverse of the display affine transformation matrix)
        mat_inv = np.linalg.inv(self.mat_affine)

        # Convert the numpy array to a tuple for affine transformation
        affine_inv = (
            mat_inv[0, 0], mat_inv[0, 1], mat_inv[0, 2],
            mat_inv[1, 0], mat_inv[1, 1], mat_inv[1, 2]
        )

        # Apply affine transformation to the PIL image data
        dst = self.original_image.transform(
            (self.original_width, self.original_height),  # Output size
            Image.AFFINE,  # Affine transformation
            affine_inv,  # Affine transformation matrix (conversion matrix from output to input)
            Image.NEAREST  # Interpolation method, nearest neighbor
        )

        # Clip the image to the canvas size
        dst = dst.crop((0, 0, canvas_width, canvas_height))

        im = ImageTk.PhotoImage(image=dst)

        # Draw the image
        self.canvas.delete("all")
        self.canvas.create_image(
            0, 0,  # Image display position (top-left coordinate)
            anchor='nw',  # Anchor, top-left is the origin
            image=im  # Display image data
        )
        self.image = im

    def redraw_image(self):
        '''Redraw the image'''
        if self.pil_image is None:
            return
        self.draw_image(self.pil_image)
        self.master.event_generate("<<RedrawPoints>>")


if __name__ == "__main__":
    root = tk.Tk()
    app = PanZoomCanvas(master=root)
    app.pack(fill=tk.BOTH, expand=True)
    app.canvas.config(bg='grey')
    app.set_image('image_path_here')
    root.mainloop()