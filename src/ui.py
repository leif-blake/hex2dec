import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QHBoxLayout, QWidget, QLabel, QRadioButton, QCheckBox,
                             QTextEdit, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

import handlers


class Hex2DecQt(QMainWindow):
    def __init__(self, version="1.0"):
        super().__init__()
        self.options_visible = False
        self.setWindowTitle(f"Hex2Dec Converter - {version}")
        self.resize(800, 600)

        # Declare UI variables
        self.hex_text = None
        self.dec_text = None
        self.bin_text = None
        self.pad_check = None
        self.prefix_check = None
        self.endian_check = None
        self.unsigned_radio = None
        self.signed_radio = None
        self.float_radio = None
        self.hex_button = None
        self.dec_button = None
        self.bin_button = None
        self.toggle_button = None

        # Main container widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # Toggle button
        self.toggle_button = QPushButton("Show Options")
        self.toggle_button.clicked.connect(self.toggle_options)
        self.main_layout.addWidget(self.toggle_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Options frame
        self.options_frame = QWidget()
        self.options_frame.setStyleSheet("background-color: #f0f0f0;")
        self.options_frame_layout = QGridLayout(self.options_frame)
        self.setup_options_widgets()

        # Initially set height to 0
        self.options_frame.setMaximumHeight(0)
        self.options_frame.setMinimumHeight(0)
        self.main_layout.addWidget(self.options_frame)

        # Animation for options frame
        self.animation = QPropertyAnimation(self.options_frame, b"maximumHeight")
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setDuration(300)

        # Conversion frame
        self.conversion_frame = QWidget()
        self.setup_conversion_widgets()
        self.main_layout.addWidget(self.conversion_frame)

        # Make conversion frame expand to fill space
        self.main_layout.setStretch(2, 1)

    def setup_options_widgets(self):
        # Checkboxes
        self.pad_check = QCheckBox("Enable Padding")
        self.pad_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.prefix_check = QCheckBox("Show Prefix")
        self.prefix_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.endian_check = QCheckBox("Little Endian")
        self.endian_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Radio buttons
        self.unsigned_radio = QRadioButton("Unsigned")
        self.unsigned_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.signed_radio = QRadioButton("Signed")
        self.signed_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.float_radio = QRadioButton("Floating Point")
        self.float_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.unsigned_radio.setChecked(True)

        # Add to layout
        self.options_frame_layout.addWidget(self.pad_check, 0, 0)
        self.options_frame_layout.addWidget(self.prefix_check, 0, 1)
        self.options_frame_layout.addWidget(self.endian_check, 0, 2)
        self.options_frame_layout.addWidget(self.unsigned_radio, 1, 0)
        self.options_frame_layout.addWidget(self.signed_radio, 1, 1)
        self.options_frame_layout.addWidget(self.float_radio, 1, 2)

    def setup_conversion_widgets(self):
        layout = QGridLayout(self.conversion_frame)

        # Hex section
        hex_label = QLabel("Hexadecimal")
        self.hex_text = QTextEdit()
        self.hex_text.installEventFilter(self)
        self.hex_button = QPushButton("Convert Hex")
        self.hex_button.clicked.connect(self.convert_hex)

        # Dec section
        dec_label = QLabel("Decimal")
        self.dec_text = QTextEdit()
        self.dec_text.installEventFilter(self)
        self.dec_button = QPushButton("Convert Decimal")
        self.dec_button.clicked.connect(self.convert_dec)

        # Bin section
        bin_label = QLabel("Binary")
        self.bin_text = QTextEdit()
        self.bin_text.installEventFilter(self)
        self.bin_button = QPushButton("Convert Binary")
        self.bin_button.clicked.connect(self.convert_bin)

        # Add to layout
        layout.addWidget(hex_label, 0, 0)
        layout.addWidget(self.hex_text, 1, 0)
        layout.addWidget(self.hex_button, 2, 0)

        layout.addWidget(dec_label, 0, 1)
        layout.addWidget(self.dec_text, 1, 1)
        layout.addWidget(self.dec_button, 2, 1)

        layout.addWidget(bin_label, 0, 2)
        layout.addWidget(self.bin_text, 1, 2)
        layout.addWidget(self.bin_button, 2, 2)

        # Set column stretch
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)

        # Set row stretch for the text edits
        layout.setRowStretch(1, 1)

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress and event.modifiers() == Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_Return:
            if obj == self.hex_text:
                self.convert_hex()
                return True
            elif obj == self.dec_text:
                self.convert_dec()
                return True
            elif obj == self.bin_text:
                self.convert_bin()
                return True
        return super().eventFilter(obj, event)

    def toggle_options(self):
        if not self.options_visible:
            # Show options
            self.options_frame.setMaximumHeight(0)  # Reset before animation
            # Get required height by temporarily removing max height constraint
            self.options_frame.setMaximumHeight(1000)
            target_height = self.options_frame.sizeHint().height()
            self.options_frame.setMaximumHeight(0)  # Reset again

            # Configure and start animation
            self.animation.setStartValue(0)
            self.animation.setEndValue(target_height)
            self.animation.start()
            self.toggle_button.setText("Hide Options")
        else:
            # Hide options
            self.animation.setStartValue(self.options_frame.height())
            self.animation.setEndValue(0)
            self.animation.start()
            self.toggle_button.setText("Show Options")

        self.options_visible = not self.options_visible

    def convert_hex(self):
        dec_result, bin_result = handlers.hex_to_other(
            self.hex_text.toPlainText(),
            self.pad_check.isChecked(),
            self.prefix_check.isChecked(),
            self.endian_check.isChecked(),
            self.unsigned_radio.isChecked(),
            self.signed_radio.isChecked(),
            self.float_radio.isChecked()
        )
        if dec_result is not None and bin_result is not None:
            self.dec_text.setPlainText(dec_result)
            self.bin_text.setPlainText(bin_result)

    def convert_dec(self):
        hex_result, dec_result, bin_result = handlers.dec_to_other(
            self.dec_text.toPlainText(),
            self.pad_check.isChecked(),
            self.prefix_check.isChecked(),
            self.endian_check.isChecked(),
            self.unsigned_radio.isChecked(),
            self.signed_radio.isChecked(),
            self.float_radio.isChecked()
        )
        if hex_result is not None and bin_result is not None and dec_result is not None:
            self.hex_text.setPlainText(hex_result)
            self.dec_text.setPlainText(dec_result)
            self.bin_text.setPlainText(bin_result)

    def convert_bin(self):
        hex_result, dec_result  = handlers.bin_to_other(
            self.bin_text.toPlainText(),
            self.pad_check.isChecked(),
            self.prefix_check.isChecked(),
            self.endian_check.isChecked(),
            self.unsigned_radio.isChecked(),
            self.signed_radio.isChecked(),
            self.float_radio.isChecked()
        )
        if dec_result is not None and hex_result is not None:
            self.dec_text.setPlainText(dec_result)
            self.hex_text.setPlainText(hex_result)
