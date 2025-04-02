"""
Entry point for the number converter application
"""

import sys

from PySide6 import QtCore
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

from ui import Hex2DecQt

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Hex2DecQt(version="0.1.1")
    # set app icon
    app_icon = QIcon()
    app_icon.addFile('res/icon16x16.png', QtCore.QSize(16, 16))
    app_icon.addFile('res/icon24x24.png', QtCore.QSize(24, 24))
    app_icon.addFile('res/icon32x32.png', QtCore.QSize(32, 32))
    app_icon.addFile('res/icon48x48.png', QtCore.QSize(48, 48))
    app_icon.addFile('res/icon256x256.png', QtCore.QSize(256, 256))
    app.setWindowIcon(app_icon)
    window.setWindowIcon(app_icon)
    window.show()
    sys.exit(app.exec())