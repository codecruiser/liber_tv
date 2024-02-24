from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class CategoryTile(QWidget):
    def __init__(self, name, size=None):
        super().__init__()
        self._v_box = QVBoxLayout()
        self._v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._label = QLabel(f"{name}")
        self._label.setWordWrap(True)
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._label.setMinimumWidth((size.width()//6)-30)
        self._label.setMinimumHeight(150)
        self._v_box.addWidget(self._label)
        self.setLayout(self._v_box)
