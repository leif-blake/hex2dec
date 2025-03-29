import tkinter as tk
from tkinter import ttk

import handlers

class Hex2Dec(tk.Tk):
    def __init__(self, version):
        super().__init__()
        self.options_visible = False
        self.title(f"Hex2Dec Converter - {version}")
        self.geometry("800x600")
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Declare widget variables
        self.toggle_button = None
        self.options_frame = None
        self.conversion_frame = None
        self.number_type_var = None
        self.little_endian_var = None
        self.show_prefix_var = None
        self.pad_var = None
        self.hex_text = None
        self.dec_text = None
        self.bin_text = None
        self.hex_button = None
        self.dec_button = None
        self.bin_button = None

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        self.toggle_button = ttk.Button(self.main_frame, text="Show Options", command=self.toggle_options)
        self.toggle_button.grid(row=0, column=0, pady=5, sticky="nw")

        self.parent_frame = ttk.Frame(self.main_frame)
        self.parent_frame.grid(row=1, column=0, pady=5, sticky="nsew")

        self.create_option_widgets()
        self.create_conversion_widgets()

        # Configure column weights
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.parent_frame.grid_columnconfigure(0, weight=1)

        # Configure row weights
        self.main_frame.grid_rowconfigure(0, weight=0)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.parent_frame.grid_rowconfigure(0, weight=0)
        self.parent_frame.grid_rowconfigure(1, weight=1)

    def create_option_widgets(self):
        self.options_frame = ttk.Frame(self.parent_frame)
        self.options_frame.grid(row=0, column=0, pady=5, sticky="nw")
        if not self.options_visible:
            self.options_frame.grid_remove()

        self.pad_var = tk.BooleanVar()
        pad_check = ttk.Checkbutton(self.options_frame, text="Enable Padding", variable=self.pad_var, takefocus=False)
        pad_check.grid(row=0, column=0, padx=5)

        self.show_prefix_var = tk.BooleanVar()
        show_prefix_check = ttk.Checkbutton(self.options_frame, text="Show Prefix", variable=self.show_prefix_var, takefocus=False)
        show_prefix_check.grid(row=0, column=1, padx=5)

        self.little_endian_var = tk.BooleanVar()
        little_endian_check = ttk.Checkbutton(self.options_frame, text="Little Endian", variable=self.little_endian_var, takefocus=False)
        little_endian_check.grid(row=0, column=2, padx=5)

        self.number_type_var = tk.StringVar(value="unsigned")

        unsigned_radio = ttk.Radiobutton(self.options_frame, text="Unsigned", variable=self.number_type_var, value="unsigned", takefocus=False)
        unsigned_radio.grid(row=1, column=0, padx=5, sticky="nw")

        signed_radio = ttk.Radiobutton(self.options_frame, text="Signed", variable=self.number_type_var, value="signed", takefocus=False)
        signed_radio.grid(row=1, column=1, padx=5, sticky="nw")

        floating_radio = ttk.Radiobutton(self.options_frame, text="Floating Point", variable=self.number_type_var, value="floating", takefocus=False)
        floating_radio.grid(row=1, column=2, padx=5, sticky="nw")

    def create_conversion_widgets(self):
        self.conversion_frame = ttk.Frame(self.parent_frame)
        self.conversion_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        hex_label = ttk.Label(self.conversion_frame, text="Hexadecimal")
        hex_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")
        self.hex_text = tk.Text(self.conversion_frame, width=20, height=15)
        self.hex_text.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.hex_button = ttk.Button(self.conversion_frame, text="Convert Hex")
        self.hex_button.grid(row=2, column=0, padx=5, pady=5)

        dec_label = ttk.Label(self.conversion_frame, text="Decimal")
        dec_label.grid(row=0, column=1, padx=5, pady=5, sticky="nw")
        self.dec_text = tk.Text(self.conversion_frame, width=20, height=15)
        self.dec_text.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")
        self.dec_button = ttk.Button(self.conversion_frame, text="Convert Decimal")
        self.dec_button.grid(row=2, column=1, padx=5, pady=5)

        bin_label = ttk.Label(self.conversion_frame, text="Binary")
        bin_label.grid(row=0, column=2, padx=5, pady=5, sticky="nw")
        self.bin_text = tk.Text(self.conversion_frame, width=20, height=15)
        self.bin_text.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")
        self.bin_button = ttk.Button(self.conversion_frame, text="Convert Binary")
        self.bin_button.grid(row=2, column=2, padx=5, pady=5)

        # Configure grid weights for resizing
        self.conversion_frame.grid_columnconfigure(0, weight=1)
        self.conversion_frame.grid_columnconfigure(1, weight=1)
        self.conversion_frame.grid_columnconfigure(2, weight=1)

        self.conversion_frame.grid_rowconfigure(0, weight=0)
        self.conversion_frame.grid_rowconfigure(1, weight=1)
        self.conversion_frame.grid_rowconfigure(2, weight=0)

        # Bind the conversion buttons to their respective functions
        # Bind handlers to buttons
        self.hex_button.config(command=lambda: handlers.hex_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                                self.little_endian_var, self.pad_var,
                                                                self.show_prefix_var))
        self.dec_button.config(command=lambda: handlers.dec_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                                self.little_endian_var, self.pad_var,
                                                                self.show_prefix_var))
        self.bin_button.config(command=lambda: handlers.bin_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                                self.little_endian_var, self.pad_var,
                                                                self.show_prefix_var))

        # Bind handlers to text boxes for shift+enter
        self.hex_text.bind("<Shift-Return>",
                           lambda event: handlers.hex_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                               self.little_endian_var, self.pad_var, self.show_prefix_var))
        self.dec_text.bind("<Shift-Return>",
                           lambda event: handlers.dec_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                               self.little_endian_var, self.pad_var, self.show_prefix_var))
        self.bin_text.bind("<Shift-Return>",
                           lambda event: handlers.bin_to_other(self.hex_text, self.dec_text, self.bin_text, self.number_type_var,
                                                               self.little_endian_var, self.pad_var, self.show_prefix_var))

    def toggle_options(self):
        if self.options_visible:
            self.animate_hide(self.options_frame)
            self.toggle_button.config(text="Show Options")
        else:
            self.options_frame.grid()
            self.animate_show(self.options_frame)
            self.toggle_button.config(text="Hide Options")
        self.options_visible = not self.options_visible

    def animate_show(self, frame, height=0):
        frame.update_idletasks()
        max_height = frame.winfo_reqheight()
        height += 5  # Smaller increment for smoother animation
        if height < max_height:
            frame.grid_configure(pady=(height, 5))
            self.after(15, self.animate_show, frame, height)  # Longer delay for smoother animation
        else:
            frame.grid_configure(pady=(max_height, 5))

    def animate_hide(self, frame, height=None):
        if height is None:
            height = frame.winfo_reqheight()
        height -= 5  # Smaller decrement for smoother animation
        if height > 0:
            frame.grid_configure(pady=(height, 5))
            self.after(15, self.animate_hide, frame, height)  # Longer delay for smoother animation
        else:
            frame.grid_remove()
