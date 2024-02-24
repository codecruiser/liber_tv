from PySide6.QtCore import Qt
from PySide6 import QtCore
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSizePolicy


class CategoryTile(QWidget):
    def __init__(self, name):
        super().__init__()
        self._v_box = QVBoxLayout()
        self._v_box.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._img = QLabel()
        self._img.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        #self._img.setMinimumSize(100, 100)
        #self._pixmap = QPixmap("images/category_test.png")
        # self._pixmap = self._pixmap.scaledToWidth(250)
        # #self._img.setPixmap(self._pixmap.scaled(self._img.frameSize(), Qt.AspectRatioMode.KeepAspectRatio))
        # self._img.setPixmap(self._pixmap)
        self._img.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self._img.setStyleSheet("""QLabel {
    border: 1px solid #333333;
    border-radius: 20px;
    padding: 2px;
    border-image: url(images/category_test.png);
}""")
        self._v_box.addWidget(self._img)
        self._label = QLabel(f"{name}")
        self._label.setWordWrap(True)
        self._label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self._v_box.addWidget(self._label)
        self.setLayout(self._v_box)
