import tkinter as tk
from tkinter import filedialog, ttk
import os
from PIL import Image, ImageTk
from zoom_utils import PanZoomCanvas

class PixelSelector:
    def __init__(self, master):
        self.master = master
        self.master.title("Pixel Selector")
        
        logo_path = "D:/DATN/tool/logo.png"
        self.logo_image = Image.open(logo_path)
        self.logo_image = self.logo_image.resize((100, 100), Image.LANCZOS)
        self.logo_image = ImageTk.PhotoImage(self.logo_image)
        
        self.menu_bar = tk.Menu(master)
        master.config(menu=self.menu_bar)
        
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Select Image Folder", command=self.select_image_folder)
        self.file_menu.add_command(label="Select Export Folder", command=self.select_export_folder)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=master.quit)
        
        self.points_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Points", menu=self.points_menu)
        self.points_menu.add_command(label="Export Points", command=self.export_points)
        self.points_menu.add_command(label="Import Points", command=self.import_points)
        
        self.main_frame = tk.Frame(master, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.logo_text_frame = tk.Frame(self.main_frame)
        self.logo_text_frame.pack(side=tk.TOP, anchor="w", pady=10)
        
        self.logo_label = tk.Label(self.logo_text_frame, image=self.logo_image)
        self.logo_label.pack(side=tk.LEFT, padx=5)
        
        self.text_frame = tk.Frame(self.logo_text_frame)
        self.text_frame.pack(side=tk.LEFT, padx=5)
        
        self.school_label_line1 = tk.Label(self.text_frame, text="    ĐẠI HỌC QUỐC GIA HÀ NỘI", font=("Arial", 16, "bold"))
        self.school_label_line1.pack(anchor="w")
        self.school_label_line2 = tk.Label(self.text_frame, text="TRƯỜNG ĐẠI HỌC CÔNG NGHỆ", font=("Arial", 16, "bold"))
        self.school_label_line2.pack(anchor="w")
        
        self.canvas_table_frame = tk.Frame(self.main_frame)
        self.canvas_table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas_frame = tk.Frame(self.canvas_table_frame)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.canvas = PanZoomCanvas(self.canvas_frame)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.table_frame = tk.Frame(self.canvas_table_frame, padx=10)
        self.table_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.pixel_info_label = tk.Label(self.table_frame, text="No image loaded", font=("Arial", 12), bg="lightgray", padx=10, pady=5)
        self.pixel_info_label.pack(pady=5)
        
        self.image_name_label = tk.Label(self.table_frame, text="", font=("Arial", 12), bg="lightgray", padx=10, pady=5)
        self.image_name_label.pack(pady=5)
        
        self.tree_scroll_y = tk.Scrollbar(self.table_frame, orient=tk.VERTICAL)
        self.tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree_scroll_x = tk.Scrollbar(self.table_frame, orient=tk.HORIZONTAL)
        self.tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(self.table_frame, columns=("Index", "X", "Y"), show="headings", height=20, yscrollcommand=self.tree_scroll_y.set, xscrollcommand=self.tree_scroll_x.set)
        self.tree.heading("Index", text="Index")
        self.tree.heading("X", text="X")
        self.tree.heading("Y", text="Y")
        self.tree.column("Index", width=50, anchor="center")
        self.tree.column("X", width=100, anchor="center")
        self.tree.column("Y", width=100, anchor="center")
        self.tree.pack(pady=5, fill=tk.BOTH, expand=True)
        
        self.tree_scroll_y.config(command=self.tree.yview)
        self.tree_scroll_x.config(command=self.tree.xview)
        
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        style.configure("Treeview", font=("Arial", 10), rowheight=25)
        
        self.tree.tag_configure('oddrow', background='lightblue')
        self.tree.tag_configure('evenrow', background='white')
        self.tree.tag_configure('highlighted', background='red')
        
        self.controls_frame = tk.Frame(self.main_frame, pady=10)
        self.controls_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.buttons_frame = tk.Frame(self.controls_frame)
        self.buttons_frame.pack(pady=5)
        
        self.delete_button = tk.Button(self.buttons_frame, text="Delete Selected Point", command=self.delete_selected_point, width=20, bg="red", fg="white", font=("Arial", 10, "bold"))
        self.delete_button.grid(row=0, column=0, padx=5, pady=5)
        
        self.prev_button = tk.Button(self.buttons_frame, text="Previous Image", command=self.prev_image, width=15, bg="blue", fg="white", font=("Arial", 10, "bold"))
        self.prev_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.next_button = tk.Button(self.buttons_frame, text="Next Image", command=self.next_image, width=15, bg="green", fg="white", font=("Arial", 10, "bold"))
        self.next_button.grid(row=0, column=2, padx=5, pady=5)
        
        self.sort_button = tk.Button(self.buttons_frame, text="Sort Points", command=self.sort_points, width=15, bg="purple", fg="white", font=("Arial", 10, "bold"))
        self.sort_button.grid(row=0, column=3, padx=5, pady=5)
        
        self.save_button = tk.Button(self.buttons_frame, text="Save Coordinates", command=self.save_coordinates, width=20, bg="orange", fg="white", font=("Arial", 10, "bold"))
        self.save_button.grid(row=0, column=4, padx=5, pady=5)
        
        self.reset_button = tk.Button(self.buttons_frame, text="Reset Image", command=self.reset_image, width=15, bg="gray", fg="white", font=("Arial", 10, "bold"))
        self.reset_button.grid(row=0, column=5, padx=5, pady=5)
        
        self.delete_all_button = tk.Button(self.buttons_frame, text="Delete All Points", command=self.delete_all_points, width=20, bg="red", fg="white", font=("Arial", 10, "bold"))
        self.delete_all_button.grid(row=0, column=6, padx=5, pady=5)
        
        self.image_files = []
        self.current_image_index = -1
        self.image = None
        self.selected_pixel = None
        self.image_points = {}
        self.current_image = None
        self.export_folder_path = None
        self.selected_pixels = []
        
        self.canvas.canvas.bind("<Button-1>", self.select_pixel)
        self.master.bind("<<RedrawPoints>>", self.redraw_points)
        
        self.master.after(60000, self.save_coordinates)
        
        self.setup_treeview_sorting()

    def select_image_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
            self.image_files.sort()
            if self.image_files:
                self.current_image_index = 0
                self.load_image()
                self.pixel_info_label.config(text=f"Loaded {len(self.image_files)} images from {folder_path}")

    def load_image(self):
        if 0 <= self.current_image_index < len(self.image_files):
            file_path = self.image_files[self.current_image_index]
            self.canvas.set_image(file_path)
            self.set_current_image(file_path)
            self.pixel_info_label.config(text=f"Loaded image: {os.path.basename(file_path)}")
            self.image_name_label.config(text=f"Image: {os.path.basename(file_path)}")
            self.redraw_points()
            self.save_coordinates()

    def prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            self.load_image()

    def next_image(self):
        if self.current_image_index < len(self.image_files) - 1:
            self.current_image_index += 1
            self.load_image()

    def select_pixel(self, event):
        if self.canvas.pil_image is not None:
            image_coords = self.canvas.to_image_point(event.x, event.y)
            if len(image_coords) > 0:
                x, y = int(image_coords[0]), int(image_coords[1])
                pixel = self.canvas.pil_image.getpixel((x, y))
                pixel_info = f"Selected pixel at ({x}, {y}): {pixel}"
                print(pixel_info)
                self.pixel_info_label.config(text=pixel_info)
                self.selected_pixel = (x, y)
                self.add_pixel_to_table(x, y)
                self.highlight_region(x, y)
                self.selected_pixels.append((x, y))

    def highlight_pixel(self, x, y, index):
        radius = 5
        canvas_coords = self.canvas.to_canvas_point(x, y)
        self.canvas.canvas.create_oval(canvas_coords[0] - radius, canvas_coords[1] - radius, canvas_coords[0] + radius, canvas_coords[1] + radius, outline="red", width=2, fill="yellow", tags=f"highlight_{x}_{y}")
        self.canvas.canvas.create_text(canvas_coords[0], canvas_coords[1], text=str(index), fill="black", font=("Arial", 8, "bold"), tags=f"highlight_{x}_{y}")

    def highlight_region(self, x, y):
        canvas_coords_top_left = self.canvas.to_canvas_point(x, y)
        canvas_coords_bottom_right = self.canvas.to_canvas_point(x + 1, y + 1)
        self.canvas.canvas.create_rectangle(
            canvas_coords_top_left[0], canvas_coords_top_left[1],
            canvas_coords_bottom_right[0], canvas_coords_bottom_right[1],
            outline="red", width=2, fill="red", tags=f"highlight_region_{x}_{y}"
        )

    def add_pixel_to_table(self, x, y):
        if self.current_image:
            self.image_points[self.current_image].append((x, y))
            self.update_treeview()
            self.pixel_info_label.config(text="Pixel added to table")

    def update_treeview(self, sort=False):
        self.tree.delete(*self.tree.get_children())
        if self.current_image:
            points = self.image_points[self.current_image]
            if sort:
                points = sorted(points, key=lambda point: (point[1], point[0]))
            for index, point in enumerate(points, start=1):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                self.tree.insert("", "end", values=(index, point[0], point[1]), tags=(tag,))
            self.redraw_points(points)

    def redraw_points(self, event=None):
        self.canvas.canvas.delete("highlight")
        self.canvas.canvas.delete("highlight_region")
        if self.current_image:
            points = self.image_points[self.current_image]
            for index, (x, y) in enumerate(points, start=1):
                self.highlight_pixel(x, y, index)
                self.highlight_region(x, y)
        self.reapply_highlights()
        self.reapply_highlights_region()

    def delete_selected_point(self):
        selected_item = self.tree.selection()
        if selected_item and self.current_image:
            self.tree.item(selected_item, tags=('highlighted',))
            self.master.after(1000, self._delete_point, selected_item)

    def _delete_point(self, selected_item):
        index = int(self.tree.item(selected_item)["values"][0]) - 1
        x, y = self.image_points[self.current_image][index]
        del self.image_points[self.current_image][index]
        self.update_treeview()
        self.pixel_info_label.config(text="Selected point deleted")
        self.canvas.canvas.delete(f"highlight_{x}_{y}")
        self.canvas.canvas.delete(f"highlight_region_{x}_{y}")
        self.redraw_points()

    def delete_all_points(self):
        if self.current_image:
            self.image_points[self.current_image] = []
            self.update_treeview()
            self.pixel_info_label.config(text="All points deleted")
            self.canvas.canvas.delete("highlight")
            self.canvas.canvas.delete("highlight_region")
            self.selected_pixels = []

    def select_export_folder(self):
        self.export_folder_path = filedialog.askdirectory()
        if self.export_folder_path:
            self.pixel_info_label.config(text=f"Export folder selected: {self.export_folder_path}")
        else:
            self.pixel_info_label.config(text="No export folder selected")

    def export_points(self):
        if self.export_folder_path:
            for image_path in self.image_files:
                image_name = os.path.basename(image_path)
                export_file_path = os.path.join(self.export_folder_path, f"{os.path.splitext(image_name)[0]}.txt")
                if image_path in self.image_points:
                    with open(export_file_path, "w") as f:
                        for index, point in enumerate(self.image_points[image_path], start=1):
                            f.write(f"{index}, {point[0]}, {point[1]}\n")
            self.pixel_info_label.config(text=f"Points exported to {self.export_folder_path}")
        else:
            self.pixel_info_label.config(text="No export folder selected")

    def import_points(self):
        if self.export_folder_path:
            for image_path in self.image_files:
                image_name = os.path.basename(image_path)
                import_file_path = os.path.join(self.export_folder_path, f"{os.path.splitext(image_name)[0]}.txt")
                if os.path.exists(import_file_path):
                    with open(import_file_path, "r") as f:
                        points = []
                        for line in f:
                            index, x, y = line.strip().split(", ")
                            points.append((float(x), float(y)))
                        self.image_points[image_path] = points
            self.update_treeview()
            self.pixel_info_label.config(text=f"Points imported from {self.export_folder_path}")
        else:
            self.pixel_info_label.config(text="No export folder selected")

    def set_current_image(self, image_id):
        self.current_image = image_id
        if image_id not in self.image_points:
            self.image_points[image_id] = []
        self.update_treeview()

    def sort_points(self):
        self.update_treeview(sort=True)

    def save_coordinates(self):
        if self.export_folder_path:
            for image_path in self.image_files:
                image_name = os.path.basename(image_path)
                export_file_path = os.path.join(self.export_folder_path, f"{os.path.splitext(image_name)[0]}.txt")
                if image_path in self.image_points:
                    with open(export_file_path, "w") as f:
                        for index, point in enumerate(self.image_points[image_path], start=1):
                            f.write(f"{index}, {point[0]}, {point[1]}\n")
            print(f"Coordinates saved to {self.export_folder_path}")
        self.master.after(60000, self.save_coordinates)

    def reset_image(self):
        if self.current_image_index >= 0:
            self.load_image()
            self.canvas.reset_transform()
            self.canvas.redraw_image()
            self.pixel_info_label.config(text="Image reset to original state")

    def reapply_highlights(self):
        for x, y in self.selected_pixels:
            self.reapply_highlights_region()

    def reapply_highlights_region(self):
        for x, y in self.selected_pixels:
            canvas_coords_top_left = self.canvas.to_canvas_point(x, y)
            canvas_coords_bottom_right = self.canvas.to_canvas_point(x + 1, y + 1)
            self.canvas.canvas.create_rectangle(
                canvas_coords_top_left[0], canvas_coords_top_left[1],
                canvas_coords_bottom_right[0], canvas_coords_bottom_right[1],
                outline="", width=0, fill="", tags=f"highlight_region_{x}_{y}"
            )
    def zoom_in(self):
        self.canvas.zoom_in()
        self.reapply_highlights()
        self.reapply_highlights_region()

    def zoom_out(self):
        self.canvas.zoom_out()
        self.reapply_highlights()
        self.reapply_highlights_region()

    def sort_treeview_column(self, col, reverse):
        items = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        items.sort(reverse=reverse)

        for index, (val, k) in enumerate(items):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda: self.sort_treeview_column(col, not reverse))
        self.update_highlights()

    def setup_treeview_sorting(self):
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col, command=lambda _col=col: self.sort_treeview_column(_col, False))

    def update_highlights(self):
        self.canvas.canvas.delete("highlight")
        self.canvas.canvas.delete("highlight_region")
        for index, item in enumerate(self.tree.get_children(''), start=1):
            x, y = self.tree.item(item, 'values')[1:3]
            self.highlight_pixel(int(x), int(y), index)