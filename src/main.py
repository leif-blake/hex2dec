"""
Entry point for the number converter application
"""

import sys
from PyQt6.QtWidgets import QApplication

from ui import Hex2DecQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Hex2DecQt(version="0.0.2")
    window.show()
    sys.exit(app.exec())