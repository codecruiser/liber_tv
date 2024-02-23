from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QStackedLayout, QPushButton, QLabel, QApplication

#from libertv.list_panel import ListPanel
from libertv.player import LibrePlayer
#from libertv.web_browser import WebBrowser


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Liber TV")

        self._stacked_layout = QStackedLayout()
        #self._list_panel = ListPanel()
        #self._stacked_layout.addWidget(self._list_panel)
        #self._stacked_layout.addWidget(WebBrowser())
        self.player = LibrePlayer()
        self._stacked_layout.addWidget(self.player)

        self._stacked_layout.addWidget(QLabel("settings"))

        self._stacked_layout.setCurrentIndex(0)
        self.setLayout(self._stacked_layout)

    def keyPressEvent(self, event):
        key = event.key()
        mod = event.modifiers()

        current_panel = self._stacked_layout.itemAt(self._stacked_layout.currentIndex()).widget()

        # if mod == QtCore.Qt.Modifier.ControlModifier and key == QtCore.Qt.Key.Key_Left:
        #     self._go_left()
        # elif mod == QtCore.Qt.Modifier.ControlModifier and key == QtCore.Qt.Key.Key_Right:
        #     print("UUUU")
        #     self._go_right()
        # elif key == QtCore.Qt.Key.Key_Right:
        #     print("ttt")
        #     if hasattr(current_panel, "go_right"):
        #         current_panel.go_right()
        # elif key == QtCore.Qt.Key.Key_Left:
        #     if hasattr(current_panel, "go_left"):
        #         current_panel.go_left()
        # elif mod == QtCore.Qt.Modifier.ShiftModifier and key == QtCore.Qt.Key.Key_Down:
        #     if hasattr(current_panel, "go_shift_down"):
        #         current_panel.go_shift_down()
        # elif key == QtCore.Qt.Key.Key_P:
        #     if hasattr(current_panel, "go_p"):
        #         current_panel.go_p()
        # elif key == QtCore.Qt.Key.Key_H:
        #     if hasattr(current_panel, "go_h"):
        #         current_panel.go_h()
        # elif key == QtCore.Qt.Key.Key_Down:
        #     if hasattr(current_panel, "go_down"):
        #         current_panel.go_down()
        # elif mod == QtCore.Qt.Modifier.ShiftModifier and key == QtCore.Qt.Key.Key_Up:
        #     if hasattr(current_panel, "go_shift_up"):
        #         current_panel.go_shift_up()
        # elif key == QtCore.Qt.Key.Key_Up:
        #     if hasattr(current_panel, "go_up"):
        #         current_panel.go_up()
        # elif mod == QtCore.Qt.Modifier.ControlModifier and key == QtCore.Qt.Key.Key_C:
        #     QApplication.quit()
        # elif key == QtCore.Qt.Key.Key_K:
        #     if hasattr(current_panel, "go_k_key"):
        #         current_panel.go_k_key()
        # elif key == QtCore.Qt.Key.Key_Return:
        #     print("ENTER!!!!")
        #     if hasattr(current_panel, "go_enter_key"):
        #         current_panel.go_enter_key()
        # else:
        #     super().keyPressEvent(event)

    def _go_left(self):
        current = self._stacked_layout.currentIndex()
        if current > 0:
            current -= 1
            self._stacked_layout.setCurrentIndex(current)

    def _go_right(self):
        current = self._stacked_layout.currentIndex()
        if current+1 < self._stacked_layout.count():
            current += 1
            self._stacked_layout.setCurrentIndex(current)

