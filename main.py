import sys

from PySide6 import QtWidgets

from libertv.main_window import MainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    with open("libretv.qss", "r") as f:
        app.setStyleSheet(f.read())
    widget = MainWindow()
    widget.resize(800, 600)
    widget.showMaximized()
    widget.showFullScreen()
    widget.show()

    sys.exit(app.exec())
