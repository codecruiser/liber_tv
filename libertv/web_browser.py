from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QWidget, QVBoxLayout


class WebBrowser(QWidget):
    def __init__(self):
        super().__init__()
        self._vbox = QVBoxLayout()
        self.web = QWebEngineView()
        self.web.load(QUrl("https://duckduckgo.com"))
        self._vbox.addWidget(self.web)
        self.setLayout(self._vbox)
