import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import os
from pathlib import Path
import threading
from datetime import datetime

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1400x700")
        
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        self.format_var = tk.StringVar(value="")
        self.dpi_var = tk.StringVar(value="")
        self.width_var = tk.StringVar(value="")
        self.height_var = tk.StringVar(value="")
        self.percentage_var = tk.StringVar(value="")
        self.aspect_ratio_var = tk.StringVar(value="")
        self.resize_mode = tk.StringVar(value="manual")  # manual, aspect, or percentage
        
        self.stop_processing = False  # Flag to stop processing
        self.tasks = []
        self.input_fields = []  # Store references to all input fields
        self.input_buttons = []  # Store references to all input buttons
        self.process_button = None  # Reference to process button
        self.stop_button = None  # Reference to stop button
        self.width_entry = None  # Reference to width entry
        self.height_entry = None  # Reference to height entry
        self.percent_entry = None  # Reference to percentage entry
        self.aspect_entry = None  # Reference to aspect ratio entry
        self.create_ui()
    
    def log_message(self, message):
        """Log message to both terminal and UI tree"""
        print(message)
        
        # Parse message type and content
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if message.startswith("[INPUT]"):
            msg_type = "Input"
            content = message.replace("[INPUT] ", "")
        elif message.startswith("[OUTPUT]"):
            msg_type = "Output"
            content = message.replace("[OUTPUT] ", "")
        elif message.startswith("[START]"):
            msg_type = "Start"
            content = message.replace("[START] ", "")
        elif message.startswith("[CONFIG]"):
            msg_type = "Config"
            content = message.replace("[CONFIG] ", "")
        elif message.startswith("[PATHS]"):
            msg_type = "Paths"
            content = message.replace("[PATHS] ", "")
        elif message.startswith("[FOLDER]"):
            msg_type = "Folder"
            content = message.replace("[FOLDER] ", "")
        elif message.startswith("[SCAN]"):
            msg_type = "Scan"
            content = message.replace("[SCAN] ", "")
        elif message.startswith("[PROCESS]"):
            msg_type = "Process"
            content = message.replace("[PROCESS] ", "")
        elif message.startswith("  [OPEN]"):
            msg_type = "Open"
            content = message.replace("  [OPEN] ", "")
        elif message.startswith("  [DPI]"):
            msg_type = "DPI"
            content = message.replace("  [DPI] ", "")
        elif message.startswith("  [RESIZE]"):
            msg_type = "Resize"
            content = message.replace("  [RESIZE] ", "")
        elif message.startswith("  [FORMAT]"):
            msg_type = "Format"
            content = message.replace("  [FORMAT] ", "")
        elif message.startswith("  [CONVERT]"):
            msg_type = "Convert"
            content = message.replace("  [CONVERT] ", "")
        elif message.startswith("  [SAVE]"):
            msg_type = "Save"
            content = message.replace("  [SAVE] ", "")
        elif message.startswith("  [NEW SIZE]"):
            msg_type = "Size"
            content = message.replace("  [NEW SIZE] ", "")
        elif message.startswith("  [SUCCESS]"):
            msg_type = "Success"
            content = message.replace("  [SUCCESS] ", "")
        elif message.startswith("  [ERROR]"):
            msg_type = "Error"
            content = message.replace("  [ERROR] ", "")
        elif message.startswith("[ERROR]"):
            msg_type = "Error"
            content = message.replace("[ERROR] ", "")
        elif message.startswith("[INFO]"):
            msg_type = "Info"
            content = message.replace("[INFO] ", "")
        else:
            msg_type = "Log"
            content = message
        
        # Insert into tree
        self.log_tree.insert("", "end", text=msg_type, values=(content, timestamp), tags=(msg_type.lower(),))
        
        # Color code different message types
        self.log_tree.tag_configure("input", foreground="blue")
        self.log_tree.tag_configure("output", foreground="blue")
        self.log_tree.tag_configure("start", foreground="green")
        self.log_tree.tag_configure("config", foreground="purple")
        self.log_tree.tag_configure("paths", foreground="gray")
        self.log_tree.tag_configure("folder", foreground="orange")
        self.log_tree.tag_configure("scan", foreground="teal")
        self.log_tree.tag_configure("process", foreground="navy")
        self.log_tree.tag_configure("open", foreground="darkgreen")
        self.log_tree.tag_configure("dpi", foreground="maroon")
        self.log_tree.tag_configure("resize", foreground="darkblue")
        self.log_tree.tag_configure("format", foreground="darkred")
        self.log_tree.tag_configure("convert", foreground="olive")
        self.log_tree.tag_configure("save", foreground="darkcyan")
        self.log_tree.tag_configure("size", foreground="sienna")
        self.log_tree.tag_configure("success", foreground="green")
        self.log_tree.tag_configure("error", foreground="red")
        self.log_tree.tag_configure("info", foreground="gray")
        self.log_tree.tag_configure("log", foreground="black")
        
        # Auto-scroll to bottom
        self.log_tree.yview_moveto(1.0)
        self.root.update_idletasks()
    
    def clear_logs(self):
        """Clear the log tree display"""
        for item in self.log_tree.get_children():
            self.log_tree.delete(item)
    
    def create_ui(self):
        # Input folder selection
        frame1 = ttk.LabelFrame(self.root, text="Input Folder", padding=10)
        frame1.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(frame1, text="Select Input Folder:").grid(row=0, column=0, sticky="w")
        input_entry1 = ttk.Entry(frame1, textvariable=self.input_folder, width=30)
        input_entry1.grid(row=0, column=1, padx=5)
        self.input_fields.append(input_entry1)
        
        browse_btn1 = ttk.Button(frame1, text="Browse", command=self.select_input_folder)
        browse_btn1.grid(row=0, column=2)
        self.input_buttons.append(browse_btn1)
        
        # Output folder selection
        frame2 = ttk.LabelFrame(self.root, text="Output Folder", padding=10)
        frame2.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(frame2, text="Select Output Folder:").grid(row=0, column=0, sticky="w")
        input_entry2 = ttk.Entry(frame2, textvariable=self.output_folder, width=30)
        input_entry2.grid(row=0, column=1, padx=5)
        self.input_fields.append(input_entry2)
        
        browse_btn2 = ttk.Button(frame2, text="Browse", command=self.select_output_folder)
        browse_btn2.grid(row=0, column=2)
        self.input_buttons.append(browse_btn2)
        
        # Processing options
        frame3 = ttk.LabelFrame(self.root, text="Processing Options", padding=10)
        frame3.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        
        ttk.Label(frame3, text="Format:").grid(row=0, column=0, sticky="w")
        format_combo = ttk.Combobox(frame3, textvariable=self.format_var, 
                    values=["", "JPG", "JPEG", "PNG", "TIF", "WEBP"], width=12)
        format_combo.grid(row=0, column=1, sticky="w", padx=5)
        self.input_fields.append(format_combo)
        
        ttk.Label(frame3, text="DPI:").grid(row=0, column=2, sticky="w")
        dpi_entry = ttk.Entry(frame3, textvariable=self.dpi_var, width=12)
        dpi_entry.grid(row=0, column=3, sticky="w", padx=5)
        self.input_fields.append(dpi_entry)
        
        # Resize mode selection
        ttk.Label(frame3, text="Resize Mode:").grid(row=1, column=0, sticky="w", pady=(10, 5))
        radio_frame = ttk.Frame(frame3)
        radio_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=(10, 5))
        
        ttk.Radiobutton(radio_frame, text="Manual Width/Height", variable=self.resize_mode, 
                       value="manual", command=self.on_resize_mode_change).pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="Aspect Ratio", variable=self.resize_mode, 
                       value="aspect", command=self.on_resize_mode_change).pack(side="left", padx=5)
        ttk.Radiobutton(radio_frame, text="Percentage", variable=self.resize_mode, 
                       value="percentage", command=self.on_resize_mode_change).pack(side="left", padx=5)
        
        ttk.Label(frame3, text="Width (px):").grid(row=2, column=0, sticky="w")
        self.width_entry = ttk.Entry(frame3, textvariable=self.width_var, width=12)
        self.width_entry.grid(row=2, column=1, sticky="w", padx=5)
        self.input_fields.append(self.width_entry)
        
        ttk.Label(frame3, text="Height (px):").grid(row=2, column=2, sticky="w")
        self.height_entry = ttk.Entry(frame3, textvariable=self.height_var, width=12)
        self.height_entry.grid(row=2, column=3, sticky="w", padx=5)
        self.input_fields.append(self.height_entry)
        
        ttk.Label(frame3, text="Resize %:").grid(row=3, column=0, sticky="w")
        self.percent_entry = ttk.Entry(frame3, textvariable=self.percentage_var, width=12)
        self.percent_entry.grid(row=3, column=1, sticky="w", padx=5)
        self.input_fields.append(self.percent_entry)
        
        ttk.Label(frame3, text="Aspect Ratio (e.g. 16:9):").grid(row=3, column=2, sticky="w")
        self.aspect_entry = ttk.Entry(frame3, textvariable=self.aspect_ratio_var, width=12)
        self.aspect_entry.grid(row=3, column=3, sticky="w", padx=5)
        self.input_fields.append(self.aspect_entry)
        
        # Bind events to calculate dimensions automatically
        self.percentage_var.trace_add('write', self.calculate_dimensions_from_percentage)
        self.aspect_ratio_var.trace_add('write', self.calculate_dimensions_from_aspect)
        self.input_folder.trace_add('write', self.on_input_folder_change)
        
        # Initialize the mode
        self.on_resize_mode_change()
        
        # Process button
        frame4 = ttk.Frame(self.root)
        frame4.grid(row=3, column=0, sticky="ew", padx=10, pady=10)
        self.process_button = ttk.Button(frame4, text="Process Images", command=self.process_images)
        self.process_button.pack(side="left", padx=5)
        self.stop_button = ttk.Button(frame4, text="Stop Processing", command=self.stop_processing_handler, state="disabled")
        self.stop_button.pack(side="left", padx=5)
        ttk.Button(frame4, text="Clear Results", command=self.clear_results).pack(side="left", padx=5)
        
        # Results table (UNDER CONTROLS IN LEFT COLUMN)
        frame5 = ttk.LabelFrame(self.root, text="Processing Results", padding=10)
        frame5.grid(row=4, column=0, rowspan=3, sticky="nsew", padx=10, pady=5)
        
        # Treeview with scrollbar
        scroll = ttk.Scrollbar(frame5)
        scroll.pack(side="right", fill="y")
        
        self.tree = ttk.Treeview(frame5, columns=("Filename", "Original Size", "New Size", "Changes", "Status"), 
                                height=20, yscrollcommand=scroll.set)
        scroll.config(command=self.tree.yview)
        
        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.column("Filename", anchor="w", width=150)
        self.tree.column("Original Size", anchor="center", width=80)
        self.tree.column("New Size", anchor="center", width=80)
        self.tree.column("Changes", anchor="w", width=150)
        self.tree.column("Status", anchor="center", width=60)
        
        self.tree.heading("#0", text="", anchor="w")
        self.tree.heading("Filename", text="Filename", anchor="w")
        self.tree.heading("Original Size", text="Original Size", anchor="center")
        self.tree.heading("New Size", text="New Size", anchor="center")
        self.tree.heading("Changes", text="Changes", anchor="w")
        self.tree.heading("Status", text="Status", anchor="center")
        
        self.tree.pack(fill="both", expand=True)
        
        # Log display as tree (RIGHT SIDE)
        frame6 = ttk.LabelFrame(self.root, text="Processing Logs", padding=10)
        frame6.grid(row=0, column=2, rowspan=7, sticky="nsew", padx=10, pady=5)
        
        # Log tree widget with scrollbar
        log_scroll = ttk.Scrollbar(frame6)
        log_scroll.pack(side="right", fill="y")
        
        self.log_tree = ttk.Treeview(frame6, columns=("Message", "Timestamp"), height=20, yscrollcommand=log_scroll.set)
        log_scroll.config(command=self.log_tree.yview)
        
        self.log_tree.column("#0", width=80, stretch=tk.NO)
        self.log_tree.column("Message", anchor="w", width=250)
        self.log_tree.column("Timestamp", anchor="center", width=80)
        
        self.log_tree.heading("#0", text="Type", anchor="w")
        self.log_tree.heading("Message", text="Message", anchor="w")
        self.log_tree.heading("Timestamp", text="Time", anchor="center")
        
        self.log_tree.pack(fill="both", expand=True)
        
        # Add clear logs button
        ttk.Button(frame6, text="Clear Logs", command=self.clear_logs).pack(side="bottom", pady=5)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)  # Process controls and results
        self.root.columnconfigure(1, weight=0)  # Empty column
        self.root.columnconfigure(2, weight=1)  # Log panel
        self.root.rowconfigure(4, weight=1)
        self.root.rowconfigure(5, weight=1)
        self.root.rowconfigure(6, weight=1)
    
    def on_input_folder_change(self, *args):
        """Recalculate dimensions when input folder changes"""
        mode = self.resize_mode.get()
        if mode == "percentage":
            self.calculate_dimensions_from_percentage()
        elif mode == "aspect":
            self.calculate_dimensions_from_aspect()
    
    def on_resize_mode_change(self):
        """Handle resize mode radio button changes"""
        mode = self.resize_mode.get()
        
        if mode == "manual":
            # Enable width/height, disable and clear others
            self.width_entry.config(state="normal")
            self.height_entry.config(state="normal")
            self.percent_entry.config(state="disabled")
            self.aspect_entry.config(state="disabled")
            self.percentage_var.set("")
            self.aspect_ratio_var.set("")
            
        elif mode == "aspect":
            # Disable width/height (will show calculated), enable aspect, disable percentage
            self.width_entry.config(state="disabled")
            self.height_entry.config(state="disabled")
            self.percent_entry.config(state="disabled")
            self.aspect_entry.config(state="normal")
            self.percentage_var.set("")
            
        elif mode == "percentage":
            # Disable width/height (will show calculated), enable percentage, disable aspect
            self.width_entry.config(state="disabled")
            self.height_entry.config(state="disabled")
            self.percent_entry.config(state="normal")
            self.aspect_entry.config(state="disabled")
            self.aspect_ratio_var.set("")
    
    def calculate_dimensions_from_percentage(self, *args):
        """Calculate and display dimensions when percentage is entered"""
        if self.resize_mode.get() != "percentage":
            return
        
        percentage_val = self.percentage_var.get().strip()
        if not percentage_val:
            self.width_var.set("")
            self.height_var.set("")
            return
        
        try:
            percentage = float(percentage_val)
            if percentage > 0:
                # Get sample image dimensions from input folder if available
                input_path = self.input_folder.get().strip()
                if input_path and os.path.exists(input_path) and os.path.isdir(input_path):
                    # Try to get first image to calculate dimensions
                    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
                    try:
                        for f in Path(input_path).iterdir():
                            if f.is_file() and f.suffix.lower() in image_extensions:
                                try:
                                    with Image.open(f) as img:
                                        w, h = img.size
                                        new_w = int(w * percentage / 100)
                                        new_h = int(h * percentage / 100)
                                        self.width_var.set(str(new_w))
                                        self.height_var.set(str(new_h))
                                        return
                                except Exception as e:
                                    continue
                    except Exception as e:
                        pass
                # If no image found, show placeholder
                self.width_var.set("Will be calculated")
                self.height_var.set("Will be calculated")
        except ValueError:
            self.width_var.set("Invalid %")
            self.height_var.set("Invalid %")
    
    def calculate_dimensions_from_aspect(self, *args):
        """Calculate and display dimensions when aspect ratio is entered"""
        if self.resize_mode.get() != "aspect":
            return
        
        aspect_val = self.aspect_ratio_var.get().strip()
        if not aspect_val:
            self.width_var.set("")
            self.height_var.set("")
            return
        
        if ':' not in aspect_val:
            self.width_var.set("")
            self.height_var.set("")
            return
        
        try:
            ar_w, ar_h = map(int, aspect_val.split(':'))
            if ar_w > 0 and ar_h > 0:
                # Get sample image dimensions from input folder if available
                input_path = self.input_folder.get().strip()
                if input_path and os.path.exists(input_path) and os.path.isdir(input_path):
                    # Try to get first image to calculate dimensions
                    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
                    try:
                        for f in Path(input_path).iterdir():
                            if f.is_file() and f.suffix.lower() in image_extensions:
                                try:
                                    with Image.open(f) as img:
                                        w, h = img.size
                                        new_h = int(w * ar_h / ar_w)
                                        self.width_var.set(str(w))
                                        self.height_var.set(str(new_h))
                                        return
                                except Exception as e:
                                    continue
                    except Exception as e:
                        pass
                # If no image found, show placeholder
                self.width_var.set("Will be calculated")
                self.height_var.set("Will be calculated")
            else:
                self.width_var.set("")
                self.height_var.set("")
        except ValueError:
            self.width_var.set("Invalid format")
            self.height_var.set("Invalid format")
    
    def disable_inputs(self):
        """Disable all input fields during processing"""
        for widget in self.input_fields:
            widget.config(state="disabled")
        for widget in self.input_buttons:
            widget.config(state="disabled")
        if self.process_button:
            self.process_button.config(state="disabled")
    
    def enable_inputs(self):
        """Enable all input fields after processing"""
        for widget in self.input_fields:
            widget.config(state="normal")
        for widget in self.input_buttons:
            widget.config(state="normal")
        if self.process_button:
            self.process_button.config(state="normal")
    
    def select_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder")
        if folder:
            self.input_folder.set(folder)
            self.log_message(f"[INPUT] Selected input folder: {folder}")
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
            self.log_message(f"[OUTPUT] Selected output folder: {folder}")
    
    def clear_results(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.tasks = []
    
    def stop_processing_handler(self):
        """Handle stop button click"""
        self.stop_processing = True
        self.stop_button.config(state="disabled")
        self.log_message("[INFO] Stop requested by user. Stopping after current image...")
    
    def validate_inputs(self):
        """Validate essential inputs and sanitize optional ones"""
        # Validate input folder
        input_path = self.input_folder.get().strip()
        if not input_path:
            return "Input folder is required"
        if not os.path.exists(input_path):
            return f"Input folder does not exist: {input_path}"
        if not os.path.isdir(input_path):
            return f"Input path is not a folder: {input_path}"

        # Validate output folder
        output_path = self.output_folder.get().strip()
        if not output_path:
            return "Output folder is required"
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path, exist_ok=True)
            except Exception as e:
                return f"Cannot create output folder: {e}"
        elif not os.path.isdir(output_path):
            return f"Output path is not a folder: {output_path}"

        # Validate optional inputs only when they have values
        # Validate DPI (only if provided)
        dpi_val = self.dpi_var.get().strip()
        if dpi_val:
            try:
                dpi_int = int(dpi_val)
                if dpi_int <= 0:
                    return f"Invalid DPI value: '{dpi_val}'. Must be a positive integer"
            except ValueError:
                return f"Invalid DPI value: '{dpi_val}'. Must be a positive integer"

        # Validate width (only if provided)
        width_val = self.width_var.get().strip()
        if width_val:
            try:
                width_int = int(width_val)
                if width_int <= 0:
                    return f"Invalid width value: '{width_val}'. Must be a positive integer"
            except ValueError:
                return f"Invalid width value: '{width_val}'. Must be a positive integer"

        # Validate height (only if provided)
        height_val = self.height_var.get().strip()
        if height_val:
            try:
                height_int = int(height_val)
                if height_int <= 0:
                    return f"Invalid height value: '{height_val}'. Must be a positive integer"
            except ValueError:
                return f"Invalid height value: '{height_val}'. Must be a positive integer"

        # Validate percentage (only if provided)
        percentage_val = self.percentage_var.get().strip()
        if percentage_val:
            try:
                percentage_float = float(percentage_val)
                if percentage_float <= 0:
                    return f"Invalid percentage value: '{percentage_val}'. Must be a positive number"
            except ValueError:
                return f"Invalid percentage value: '{percentage_val}'. Must be a positive number"

        # Validate aspect ratio (only if provided)
        aspect_val = self.aspect_ratio_var.get().strip()
        if aspect_val:
            if ':' not in aspect_val:
                return f"Invalid aspect ratio format: '{aspect_val}'. Must be in format 'width:height' (e.g., 16:9)"
            else:
                try:
                    ar_w, ar_h = map(int, aspect_val.split(':'))
                    if ar_w <= 0 or ar_h <= 0:
                        return f"Invalid aspect ratio value: '{aspect_val}'. Must be two positive integers separated by ':'"
                except ValueError:
                    return f"Invalid aspect ratio value: '{aspect_val}'. Must be two positive integers separated by ':'"

        # Validate based on selected resize mode
        resize_mode = self.resize_mode.get()
        
        if resize_mode == "manual":
            # Manual mode: can have width and/or height
            # Already validated above
            pass
        elif resize_mode == "percentage":
            # Percentage mode: must have percentage value
            if not percentage_val:
                return "Please enter a percentage value for resize"
        elif resize_mode == "aspect":
            # Aspect ratio mode: must have aspect ratio value
            if not aspect_val:
                return "Please enter an aspect ratio (e.g., 16:9)"

        return None  # No errors
    
    def process_images(self):
        # Validate inputs before processing
        validation_error = self.validate_inputs()
        if validation_error:
            messagebox.showerror("Validation Error", validation_error)
            self.log_message(f"[ERROR] {validation_error}")
            return
        
        # Reset stop flag and enable stop button
        self.stop_processing = False
        self.stop_button.config(state="normal")
        
        # Disable all inputs during processing
        self.disable_inputs()
        
        self.log_message(f"\n[START] Beginning image processing...")
        self.log_message(f"[CONFIG] Format: {self.format_var.get() or 'Original'}")
        self.log_message(f"[CONFIG] DPI: {self.dpi_var.get() or 'Default'}")
        self.log_message(f"[CONFIG] Width: {self.width_var.get() or 'Not set'}")
        self.log_message(f"[CONFIG] Height: {self.height_var.get() or 'Not set'}")
        self.log_message(f"[CONFIG] Percentage: {self.percentage_var.get() or 'Not set'}")
        self.log_message(f"[CONFIG] Aspect Ratio: {self.aspect_ratio_var.get() or 'Not set'}")
        
        # Run processing in background thread
        thread = threading.Thread(target=self._process_images_thread)
        thread.start()
    
    def _process_images_thread(self):
        input_path = Path(self.input_folder.get())
        output_path = Path(self.output_folder.get())
        
        self.log_message(f"[PATHS] Input: {input_path}")
        self.log_message(f"[PATHS] Output: {output_path}")
        
        # Create output folder if it doesn't exist
        try:
            output_path.mkdir(parents=True, exist_ok=True)
            self.log_message(f"[FOLDER] Output folder ready: {output_path}")
        except Exception as e:
            self.log_message(f"[ERROR] Failed to create output folder: {e}")
            return
        
        # Get image files
        image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.tif'}
        image_files = [f for f in input_path.iterdir() if f.suffix.lower() in image_extensions]
        
        self.log_message(f"[SCAN] Found {len(image_files)} image(s) in input folder")
        
        if not image_files:
            messagebox.showinfo("Info", "No image files found in the selected folder")
            self.log_message("[INFO] No image files found")
            self.stop_button.config(state="disabled")
            self.enable_inputs()
            return
        
        for idx, image_file in enumerate(image_files, 1):
            # Check if stop was requested
            if self.stop_processing:
                self.log_message(f"\n[INFO] Processing stopped by user at image {idx}/{len(image_files)}")
                break
            
            self.log_message(f"\n[PROCESS] [{idx}/{len(image_files)}] Processing: {image_file.name}")
            self._process_single_image(image_file, output_path)
        
        # Processing complete - re-enable inputs and disable stop button
        if self.stop_processing:
            self.log_message(f"\n[END] Image processing stopped! Processed {idx-1} of {len(image_files)} images.")
        else:
            self.log_message(f"\n[END] Image processing completed!")
        
        self.stop_button.config(state="disabled")
        self.enable_inputs()
    
    def _process_single_image(self, image_file, output_path):
        try:
            img = Image.open(image_file)
            original_size = img.size
            self.log_message(f"  [OPEN] Opened image - Size: {original_size[0]}x{original_size[1]}, Mode: {img.mode}, Format: {img.format}")
            changes = {}
            
            # Get DPI
            dpi_val = self.dpi_var.get()
            if dpi_val:
                changes["dpi"] = dpi_val
                self.log_message(f"  [DPI] Setting DPI to {dpi_val}")
            
            # Resize
            if self.width_var.get() and self.height_var.get():
                w = int(self.width_var.get())
                h = int(self.height_var.get())
                img = img.resize((w, h))
                changes["size"] = f"{w}x{h}"
                self.log_message(f"  [RESIZE] Resized to {w}x{h}")
            elif self.percentage_var.get():
                percentage = float(self.percentage_var.get())
                w, h = img.size
                new_w = int(w * percentage / 100)
                new_h = int(h * percentage / 100)
                img = img.resize((new_w, new_h))
                changes["size"] = f"{percentage}% -> {new_w}x{new_h}"
                self.log_message(f"  [RESIZE] Scaled by {percentage}% -> {new_w}x{new_h}")
            elif self.aspect_ratio_var.get():
                aspect_ratio = self.aspect_ratio_var.get()
                w, h = img.size
                ar_w, ar_h = map(int, aspect_ratio.split(':'))
                new_h = int(w * ar_h / ar_w)
                img = img.resize((w, new_h))
                changes["size"] = f"aspect {aspect_ratio} -> {w}x{new_h}"
                self.log_message(f"  [RESIZE] Applied aspect ratio {aspect_ratio} -> {w}x{new_h}")
            
            # Convert format
            format_val = self.format_var.get()
            if format_val:
                self.log_message(f"  [FORMAT] Converting to {format_val}")
                if format_val.upper() in ['JPEG', 'JPG'] and img.mode != 'RGB':
                    img = img.convert('RGB')
                    self.log_message(f"  [CONVERT] Converted image mode to RGB for JPEG")
                
                format_upper = format_val.upper()
                format_map = {
                    'JPG': 'JPEG',
                    'JPEG': 'JPEG',
                    'PNG': 'PNG',
                    'TIF': 'TIFF',
                    'TIFF': 'TIFF',
                    'WEBP': 'WEBP'
                }
                pil_format = format_map.get(format_upper, format_upper)
                extension = format_upper.lower() if format_upper != 'TIFF' else 'tif'
                output_filename = f"{image_file.stem}.{extension}"
                output_file = output_path / output_filename
                
                self.log_message(f"  [SAVE] Saving as {pil_format} to {output_file}")
                if dpi_val:
                    img.save(output_file, pil_format, dpi=(int(dpi_val), int(dpi_val)))
                else:
                    img.save(output_file, pil_format)
                
                changes["format"] = pil_format
            else:
                extension = image_file.suffix.lower().lstrip('.')
                output_filename = image_file.name
                output_file = output_path / output_filename
                
                self.log_message(f"  [SAVE] Saving with original format to {output_file}")
                if dpi_val:
                    img.save(output_file, dpi=(int(dpi_val), int(dpi_val)))
                else:
                    img.save(output_file)
            
            self.log_message(f"  [NEW SIZE] {img.size[0]}x{img.size[1]}")
            
            # Add to results
            task = {
                "filename": image_file.name,
                "original_size": f"{original_size[0]}x{original_size[1]}",
                "new_size": f"{img.size[0]}x{img.size[1]}",
                "changes": changes,
                "status": "✓ Completed"
            }
            self.tasks.append(task)
            self._update_table(task)
            self.log_message(f"  [SUCCESS] Image processed successfully")
        
        except Exception as e:
            self.log_message(f"  [ERROR] Failed to process: {str(e)}")
            task = {
                "filename": image_file.name,
                "original_size": "N/A",
                "new_size": "N/A",
                "changes": {},
                "status": f"✗ Failed: {str(e)}"
            }
            self.tasks.append(task)
            self._update_table(task)
    
    def _update_table(self, task):
        changes_str = ", ".join([f"{k}: {v}" for k, v in task["changes"].items()])
        status_color = "green" if "Completed" in task["status"] else "red"
        
        item_id = self.tree.insert("", "end", values=(
            task["filename"],
            task["original_size"],
            task["new_size"],
            changes_str,
            task["status"]
        ))
        
        # Color the status cell
        if "Completed" in task["status"]:
            self.tree.item(item_id, tags=("completed",))
        else:
            self.tree.item(item_id, tags=("failed",))
        
        self.tree.tag_configure("completed", foreground="green")
        self.tree.tag_configure("failed", foreground="red")


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()