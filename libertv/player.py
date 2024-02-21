from PySide2 import QtGui, QtCore
import sys

from PySide2.QtCore import QUrl, QSize, QSizeF, Qt
from PySide2.QtGui import QColor, QBrush
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtMultimediaWidgets import QVideoWidget, QGraphicsVideoItem
from PySide2.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QApplication, QGraphicsTextItem, QGraphicsRectItem


class LibrePlayer(QWidget):

    status_template = "<div style='display:block;background-color:#666666;border-radius:20px;font-size:40px;padding:10px 20px;'>{}</div>"
    timer_template = "<div style='display:block;background-color:#333333;border-radius:20px;font-size:28px;padding:10px 20px;'>{} / {}</div>"
    bufor_template = "<div style='display:block;background-color:#666666;border-radius:20px;font-size:28px;padding:10px 20px;'>{}</div>"

    def __init__(self):
        super().__init__()
        self.player = QMediaPlayer()
        self.showMaximized()
        size = self.screen().availableGeometry().size()
        self.setContentsMargins(0, 0, 0, 0)

        # attach signals
        self.player.bufferStatusChanged.connect(self.check_buffer)
        self.player.positionChanged.connect(self.position_changed)
        self.player.playbackRateChanged.connect(self.playback_rate)
        self.player.volumeChanged.connect(self.volume_changed)
        self.player.error.connect(self.callback_error)

        self.video_widget = QGraphicsVideoItem()
        self.video_widget.setSize(QSize(size.width(), size.height()))
        self.player.setVideoOutput(self.video_widget)

        self.scene = QGraphicsScene(self)
        self.paint_black_background()
        self.scene.addItem(self.video_widget)
        self.paint_information_panel(size)

        self.view = QGraphicsView(self.scene, self)
        self.view.setMinimumWidth(size.width())
        self.view.setMinimumHeight(size.height())
        self.view.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.view.show()
        self.show()

    def paint_information_panel(self, size):
        self.bufor_label = QGraphicsTextItem()
        self.bufor_label.setDefaultTextColor(QColor(250, 250, 250, 255))
        self.bufor_label.setX(700)
        self.bufor_label.setY(size.height()-100)
        self.bufor_label.setHtml(self.bufor_template.format("Bufor"))
        self.scene.addItem(self.bufor_label)

        self.time_counter = QGraphicsTextItem()
        self.time_counter.setDefaultTextColor(QColor(250, 250, 250, 255))
        self.time_counter.setX(1200)
        self.time_counter.setY(size.height()-100)
        self.time_counter.setHtml(self.timer_template.format("--:--:--", "--:--:--"))
        self.scene.addItem(self.time_counter)

        self.status_label = QGraphicsTextItem()
        self.status_label.setDefaultTextColor(QColor(250, 250, 250, 255))
        self.status_label.setX(100)
        self.status_label.setY(size.height() - 100)
        self.status_label.setHtml(self.status_template.format("\u23F8"))
        self.scene.addItem(self.status_label)

    def paint_black_background(self):
        size = self.screen().availableGeometry().size()
        rect = QGraphicsRectItem(0, 0, size.width(), size.height())

        rect.setPos(0, 0)
        brush = QBrush(Qt.black)
        rect.setBrush(brush)

        self.scene.addItem(rect)

    def play(self, url):
        self.player.setMedia(QUrl(url))
        self.player.play()

    def toggle_play(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.status_label.setHtml(self.status_template.format("\u23F8"))
        else:
            self.player.play()
            self.status_label.setHtml(self.status_template.format("\u23F5"))

    def check_buffer(self, m):
        if m < 100:
            self.status_label.setHtml(self.status_template.format("\u23F3"))
        else:
            self.status_label.setHtml(self.status_template.format("\u23F5"))
        self.bufor_label.setHtml(self.bufor_template.format(f"{m}% wczytano"))

    def position_changed(self, ms):
        base_sek = ms//1000
        sek = base_sek % 60
        base_min = base_sek//60
        min = base_min % 60
        hr = base_min // 60
        self.time_counter.setHtml(self.timer_template.format(f"{hr:02d}:{min:02d}:{sek:02d}", "--:--:--"))

    def playback_rate(self, m):
        print(m)

    def volume_changed(self, m):
        print(m)

    def callback_error(self, error):
        self.bufor_label.setHtml(self.bufor_template.format(error))

    def go_p(self):
        # stream test
        # self.play(
        #     "https://stream-10.ix7.dailymotion.com/sec(1nXeBFcLxi2SiPaUv6X4gaw8c7wOaljv1iTukzy7oAAX74B8jqyrK4VEIPLXnCr-)/dm/3/x3b68jn/d/live-2.m3u8#cell=lcore"
        # )
        # fixed-length video test
        self.play("https://vod.idnes.cz/a/2402/14/VF240214_120155_flv_high_iri.mp4")

    def go_h(self):
        if self.bufor_label.isVisible():
            self.bufor_label.hide()
            self.time_counter.hide()
            self.status_label.hide()
        else:
            self.bufor_label.show()
            self.time_counter.show()
            self.status_label.show()

    def go_right(self):
        print("zzz")
        print(self.player.position())
        #self.player.setPosition(self.player.position())

    def go_left(self):
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    libre_player = LibrePlayer()
    #libre_player.play("https://vod.idnes.cz/a/2402/14/VF240214_120155_flv_high_iri.mp4")
    libre_player.play("https://stream-10.ix7.dailymotion.com/sec(1nXeBFcLxi2SiPaUv6X4gaw8c7wOaljv1iTukzy7oAAX74B8jqyrK4VEIPLXnCr-)/dm/3/x3b68jn/d/live-2.m3u8#cell=lcore")
    sys.exit(app.exec_())
