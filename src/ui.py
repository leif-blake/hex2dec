import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout,
                             QHBoxLayout, QWidget, QLabel, QRadioButton, QCheckBox,
                             QTextEdit, QGridLayout)
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

import handlers
from settings import Settings


class Hex2DecQt(QMainWindow):
    def __init__(self, version="1.0"):
        super().__init__()

        # Import settings
        self.settings = Settings()
        self.settings.load_settings()

        self.options_visible = self.settings.get_setting(['showQuickOptions'])
        self.setWindowTitle(f"Hex2Dec Converter - {version}")
        self.resize(self.settings.get_setting(['screenSize', 'width']),
                    self.settings.get_setting(['screenSize', 'height']))

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
        if self.options_visible:
            self.toggle_button = QPushButton("Hide Options (o)")
        else:
            self.toggle_button = QPushButton("Show Options (o)")
        self.toggle_button.clicked.connect(self.toggle_options)
        self.main_layout.addWidget(self.toggle_button, alignment=Qt.AlignmentFlag.AlignLeft)

        # Options frame
        self.options_frame = QWidget()
        self.options_frame.setStyleSheet("background-color: #f0f0f0;")
        self.options_frame_layout = QGridLayout(self.options_frame)
        self.setup_options_widgets()

        self.load_quick_options(self.settings)

        if not self.options_visible:
            self.options_frame.setMaximumHeight(0)
            self.options_frame.setMinimumHeight(0)
        self.main_layout.addWidget(self.options_frame)

        # Animation for options frame
        self.animation = QPropertyAnimation(self.options_frame, b"maximumHeight")
        self.animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animation.setDuration(200)

        # Conversion frame
        self.conversion_frame = QWidget()
        self.setup_conversion_widgets()
        self.main_layout.addWidget(self.conversion_frame)

        # Make conversion frame expand to fill space
        self.main_layout.setStretch(2, 1)

        # Push the default state
        self.quick_options_history = []
        self.hex_text_history = []
        self.dec_text_history = []
        self.bin_text_history = []
        self.history_index = 0
        self.push_state()

    def setup_options_widgets(self):
        # Checkboxes
        self.pad_check = QCheckBox("Enable Padding (p)")
        self.pad_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.prefix_check = QCheckBox("Show Prefix (k)")
        self.prefix_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.endian_check = QCheckBox("Little Endian (n)")
        self.endian_check.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Radio buttons
        self.unsigned_radio = QRadioButton("Unsigned (u)")
        self.unsigned_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.signed_radio = QRadioButton("Signed (s)")
        self.signed_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.float_radio = QRadioButton("Floating Point (l)")
        self.float_radio.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.unsigned_radio.setChecked(True)

        # Add to layout
        self.options_frame_layout.addWidget(self.pad_check, 0, 0)
        self.options_frame_layout.addWidget(self.prefix_check, 0, 1)
        self.options_frame_layout.addWidget(self.endian_check, 0, 2)
        self.options_frame_layout.addWidget(self.unsigned_radio, 1, 0)
        self.options_frame_layout.addWidget(self.signed_radio, 1, 1)
        self.options_frame_layout.addWidget(self.float_radio, 1, 2)

        # Add label in bottom right corner indicating shift-enter for conversion
        shift_enter_label = QLabel("Press Shift+Enter to convert, Ctrl+Z/Y to undo/redo")
        shift_enter_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.options_frame_layout.addWidget(shift_enter_label, 2, 0, 1, 3)

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

    def load_quick_options(self, settings: Settings):
        # Load settings from the Settings object
        self.pad_check.setChecked(settings.get_setting(['quickOptions', 'pad']))
        self.prefix_check.setChecked(settings.get_setting(['quickOptions', 'prefix']))
        self.endian_check.setChecked(settings.get_setting(['quickOptions', 'endianness']) == "little")
        default_type = settings.get_setting(['quickOptions', 'defaultType'])
        if default_type == "unsigned":
            self.unsigned_radio.setChecked(True)
        elif default_type == "signed":
            self.signed_radio.setChecked(True)
        elif default_type == "floating":
            self.float_radio.setChecked(True)
        else:
            self.unsigned_radio.setChecked(True)

    def set_qick_options(self, settings):
        # Set the quick options in settings based on the current state of the checkboxes and radio buttons
        settings.set_setting(['showQuickOptions'], self.options_visible)

        settings.set_setting(['quickOptions', 'pad'], self.pad_check.isChecked())
        settings.set_setting(['quickOptions', 'prefix'], self.prefix_check.isChecked())
        settings.set_setting(['quickOptions', 'endianness'], "little" if self.endian_check.isChecked() else "big")
        settings.set_setting(['quickOptions', 'defaultType'],
                                  "unsigned" if self.unsigned_radio.isChecked() else "signed" if self.signed_radio.isChecked() else "floating")

        settings.set_setting(['screenSize', 'width'], self.width())
        settings.set_setting(['screenSize', 'height'], self.height())


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
            self.toggle_button.setText("Hide Options (o)")
        else:
            # Hide options
            self.animation.setStartValue(self.options_frame.height())
            self.animation.setEndValue(0)
            self.animation.start()
            self.toggle_button.setText("Show Options (o)")

        self.options_visible = not self.options_visible

    def convert_hex(self):
        hex_result, dec_result, bin_result = handlers.hex_to_other(
            self.hex_text.toPlainText(),
            self.pad_check.isChecked(),
            self.prefix_check.isChecked(),
            self.endian_check.isChecked(),
            self.unsigned_radio.isChecked(),
            self.signed_radio.isChecked(),
            self.float_radio.isChecked()
        )
        if hex_result is not None and bin_result is not None and dec_result is not None:
            self.hex_text.setPlainText(hex_result)
            self.hex_text.moveCursor(self.hex_text.textCursor().MoveOperation.End)
            self.dec_text.setPlainText(dec_result)
            self.bin_text.setPlainText(bin_result)
            self.push_state()

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
            self.dec_text.moveCursor(self.dec_text.textCursor().MoveOperation.End)
            self.bin_text.setPlainText(bin_result)
            self.push_state()

    def convert_bin(self):
        hex_result, dec_result, bin_result  = handlers.bin_to_other(
            self.bin_text.toPlainText(),
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
            self.bin_text.moveCursor(self.bin_text.textCursor().MoveOperation.End)
            self.push_state()

    def eventFilter(self, obj, event):
        if event.type() == event.Type.KeyPress:
            if event.modifiers() == Qt.KeyboardModifier.ShiftModifier and event.key() == Qt.Key.Key_Return:
                if obj == self.hex_text:
                    self.convert_hex()
                    return True
                elif obj == self.dec_text:
                    self.convert_dec()
                    return True
                elif obj == self.bin_text:
                    self.convert_bin()
                    return True
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Z:
                self.load_previous_state()
                return True
            elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Y:
                self.load_next_state()
                return True
            elif event.key() == Qt.Key.Key_Backtab:
                if obj == self.hex_text:
                    self.bin_text.setFocus()
                    return True
                elif obj == self.dec_text:
                    self.hex_text.setFocus()
                    return True
                elif obj == self.bin_text:
                    self.dec_text.setFocus()
                    return True
            elif event.key() == Qt.Key.Key_Tab:
                if obj == self.hex_text:
                    self.dec_text.setFocus()
                    return True
                elif obj == self.dec_text:
                    self.bin_text.setFocus()
                    return True
                elif obj == self.bin_text:
                    self.hex_text.setFocus()
                    return True
            # 'o' to toggle options
            elif event.key() == Qt.Key.Key_O:
                self.toggle_options()
                return True
            elif event.key() == Qt.Key.Key_P:
                self.pad_check.setChecked(not self.pad_check.isChecked())
                return True
            elif event.key() == Qt.Key.Key_K:
                self.prefix_check.setChecked(not self.prefix_check.isChecked())
                return True
            elif event.key() == Qt.Key.Key_N:
                self.endian_check.setChecked(not self.endian_check.isChecked())
                return True
            elif event.key() == Qt.Key.Key_U:
                self.unsigned_radio.setChecked(True)
                return True
            elif event.key() == Qt.Key.Key_S:
                self.signed_radio.setChecked(True)
                return True
            elif event.key() == Qt.Key.Key_L:
                self.float_radio.setChecked(True)
                return True

        return super().eventFilter(obj, event)

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Z:
            self.load_previous_state()
            return
        elif event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Y:
            self.load_next_state()
            return
        elif event.key() == Qt.Key.Key_O:
            self.toggle_options()
            return
        elif event.key() == Qt.Key.Key_P:
            self.pad_check.setChecked(not self.pad_check.isChecked())
            return
        elif event.key() == Qt.Key.Key_K:
            self.prefix_check.setChecked(not self.prefix_check.isChecked())
            return
        elif event.key() == Qt.Key.Key_N:
            self.endian_check.setChecked(not self.endian_check.isChecked())
            return
        elif event.key() == Qt.Key.Key_U:
            self.unsigned_radio.setChecked(True)
            return
        elif event.key() == Qt.Key.Key_S:
            self.signed_radio.setChecked(True)
            return
        elif event.key() == Qt.Key.Key_L:
            self.float_radio.setChecked(True)
            return
        super().keyPressEvent(event)

    def push_state(self):
        # If not most recent state, remove all states after the current index
        if self.history_index < len(self.quick_options_history) - 1:
            self.quick_options_history = self.quick_options_history[:self.history_index + 1]
            self.hex_text_history = self.hex_text_history[:self.history_index + 1]
            self.dec_text_history = self.dec_text_history[:self.history_index + 1]
            self.bin_text_history = self.bin_text_history[:self.history_index + 1]

        # Save the current quick options and conversion text
        settings = Settings()
        self.set_qick_options(settings)
        self.quick_options_history.append(settings)
        self.hex_text_history.append(self.hex_text.toPlainText())
        self.dec_text_history.append(self.dec_text.toPlainText())
        self.bin_text_history.append(self.bin_text.toPlainText())

        # Limit the history to the last 100 states
        if len(self.quick_options_history) > 100:
            self.quick_options_history.pop(0)
            self.hex_text_history.pop(0)
            self.dec_text_history.pop(0)
            self.bin_text_history.pop(0)

        self.history_index = len(self.quick_options_history) - 1

    def load_state_by_index(self, index):
        # Load the state at the given index
        if len(self.quick_options_history) == 0 or index < 0 or index >= len(self.quick_options_history):
            return

        settings = self.quick_options_history[index]
        self.load_quick_options(settings)
        self.hex_text.setPlainText(self.hex_text_history[index])
        self.dec_text.setPlainText(self.dec_text_history[index])
        self.bin_text.setPlainText(self.bin_text_history[index])

    def load_previous_state(self):
        # Load the previous state if it exists
        if self.history_index > 0:
            self.history_index -= 1
            self.load_state_by_index(self.history_index)

    def load_next_state(self):
        # Load the next state if it exists
        if self.history_index < len(self.quick_options_history) - 1:
            self.history_index += 1
            self.load_state_by_index(self.history_index)

    def closeEvent(self, event):
        # Save settings
        self.set_qick_options(self.settings)

        self.settings.save_settings()
        super().closeEvent(event)

