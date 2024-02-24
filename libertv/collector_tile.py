from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class CollectorTile(QWidget):
    def __init__(self, name):
        super().__init__()
        self._v_box = QVBoxLayout()
        self._v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._label = QLabel(f"{name}")
        self._label.setWordWrap(True)
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._v_box.addWidget(self._label)
        self.setLayout(self._v_box)
