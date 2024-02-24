"""
NOTE!!
This module can be included or set deprecated - it depends on how difficult it will be to marry vlc player embedding
with Wayland on Ubuntu. Initially I wanted to use it but failed with Ubuntu update ie. switch from X to Wayland.
"""

import time

import vlc
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import QWidget, QFrame, QVBoxLayout, QLabel


class VLCPlayer(QWidget):

    def __init__(self):
        super().__init__()
        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.videoframe = QFrame()
        self.videoframe.setAutoFillBackground(True)

        self.vboxlayout = QVBoxLayout()
        self.label = QLabel("jakis text")
        self.label.hide()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.label)

        self.setLayout(self.vboxlayout)
        self.mediaplayer.set_xwindow(self.videoframe.winId())
        self.is_paused = False

    def open_file(self):
        self.mediaplayer.set_mrl("https://rr4---sn-u2oxu-f5fed.googlevideo.com/videoplayback?expire=1704255411&ei=U4uUZeKPD9jQ6dsP9Z6s-Ao&ip=31.61.239.155&id=o-AIGzD8N4TUZSfoOyypQum-al5zOOQypWQ7B3Y4Uxg5Ph&itag=135&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C271%2C278%2C313&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=9F&mm=31%2C26&mn=sn-u2oxu-f5fed%2Csn-4g5ednse&ms=au%2Conr&mv=m&mvi=4&pl=27&initcwndbps=540000&spc=UWF9f1Cq1tlBQAXBx2tKWukL5tRyE4GKvd8On-UjUw&vprv=1&svpuc=1&mime=video%2Fmp4&ns=bwLenYkW2oT-0H0cA1slVEQQ&gir=yes&clen=133569371&dur=3593.790&lmt=1704033462121439&mt=1704232864&fvip=5&keepalive=yes&fexp=24007246&c=WEB&txp=4432434&n=_qBWtYosdxoN7G_YVhXW&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIgY6QhuAWt0BXYh1S9E5z-oOsZd0j06sbUrmVD5I-E9HACIQCwAizT14e6yoRiijj8J3PJoMvYix9ajpKjcRd2TkD56Q%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AAO5W4owRAIgSp6N_FfBUEO0R7iYP-4I_E-F6XF92fJCbc6aTG3qG1ACIEWwOYIVfZhv2qKJkvVnUVJfnAbMfbiHTKZ_-W1ksog3")

        self.mediaplayer.add_slave(1, "https://rr4---sn-u2oxu-f5fed.googlevideo.com/videoplayback?expire=1704255411&ei=U4uUZeKPD9jQ6dsP9Z6s-Ao&ip=31.61.239.155&id=o-AIGzD8N4TUZSfoOyypQum-al5zOOQypWQ7B3Y4Uxg5Ph&itag=140&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=9F&mm=31%2C26&mn=sn-u2oxu-f5fed%2Csn-4g5ednse&ms=au%2Conr&mv=m&mvi=4&pl=27&initcwndbps=540000&spc=UWF9f1Cq1tlBQAXBx2tKWukL5tRyE4GKvd8On-UjUw&vprv=1&svpuc=1&mime=audio%2Fmp4&ns=bwLenYkW2oT-0H0cA1slVEQQ&gir=yes&clen=58163048&dur=3593.845&lmt=1704029846508446&mt=1704232864&fvip=5&keepalive=yes&fexp=24007246&c=WEB&txp=4432434&n=_qBWtYosdxoN7G_YVhXW&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cxpc%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIhAM_p_qmQb2RI8T8MoaOhf8I6lxuxxN1DpHqm06Owef6NAiB-NFBUQTvIU3ZL1az15BW3udf1dpjsKmY3gwe4Pv9GuA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AAO5W4owRAIgSp6N_FfBUEO0R7iYP-4I_E-F6XF92fJCbc6aTG3qG1ACIEWwOYIVfZhv2qKJkvVnUVJfnAbMfbiHTKZ_-W1ksog3", True)
        #self.mediaplayer.add_slave(0, 'test.srt', True)
        self.mediaplayer.play()

        self.setWindowTitle(self.media.get_meta(vlc.Meta.Title))

        self.mediaplayer.set_hwnd(int(self.videoframe.winId()))

    def go_k_key(self):
        print("......")
        self.open_file()

    def go_p_key(self):
        if self.label.isVisible():
            self.label.hide()
        else:
            self.label.show()


# class VLCPlayer(QWidget):
#
#     def __init__(self):
#         super().__init__()
#         self.instance = vlc.Instance(
#             "-A=alsa", "--alsa-audio-device=default", "--no-xlib", "--input-repeat=-1",
#             "--file-caching=30000", "--network-caching=30000"
#         )
#         self.media = None
#
#         self.mediaplayer = self.instance.media_player_new()
#         self.videoframe = QFrame()
#
#         self.palette = self.videoframe.palette()
#         self.palette.setColor(QPalette.Window, QColor(0, 0, 0))
#         self.videoframe.setPalette(self.palette)
#         self.videoframe.setAutoFillBackground(True)
#         self.vboxlayout = QVBoxLayout()
#         self.vboxlayout.addWidget(self.videoframe)
#         self.mediaplayer.set_xwindow(self.videoframe.winId())
#         self.set_audio_video()
#
#     def go_k_key(self):
#         print("......")
#         self.set_audio_video()
#
#     def set_audio_video(self, video_url=None, audio_url=None):
#         self.mediaplayer.set_mrl("https://rr4---sn-u2oxu-f5fed.googlevideo.com/videoplayback?expire=1704157581&ei=LQ2TZdWyLIODi9oPk6ibwAw&ip=31.61.237.144&id=o-ADQVwUZnRa0WA2Uz_B1iB75qma_98bCcRehSPrYYjyFv&itag=135&aitags=133%2C134%2C135%2C136%2C137%2C160%2C242%2C243%2C244%2C247%2C248%2C271%2C278%2C313&source=youtube&requiressl=yes&xpc=EgVo2aDSNQ%3D%3D&mh=9F&mm=31%2C26&mn=sn-u2oxu-f5fed%2Csn-c0q7lnz7&ms=au%2Conr&mv=m&mvi=4&pl=21&initcwndbps=452500&spc=UWF9f87nlrzdqQsf80q9aGR7a8nniO71iozZy-QYAQ&vprv=1&svpuc=1&mime=video%2Fmp4&ns=My7tvsEp-F9bzPbp2v7guZUQ&gir=yes&clen=133569371&dur=3593.790&lmt=1704033462121439&mt=1704135668&fvip=1&keepalive=yes&fexp=24007246&c=WEB&txp=4432434&n=QcmWseegqVaKIPQE0CSr&sparams=expire%2Cei%2Cip%2Cid%2Caitags%2Csource%2Crequiressl%2Cxpc%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Cgir%2Cclen%2Cdur%2Clmt&sig=AJfQdSswRQIgKZj8hNNjNHhp_6980lRv8Fhkw5Rft-YSckAQCvf2DTUCIQCAHbmd8XgelUNsjGKWuouF80YtXtOjVlCQ5pKpKL6Iow%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AAO5W4owRAIgHBXxYLs2g3xiPzGkRKZEWMkolV20jsuMmiUt0o-WsEQCIHgWqM39LyeHxiqcV1ZRZCNoKKayCmqRjgW0D_6cin64")
#
#         self.mediaplayer.play()
#
#         self.setWindowTitle(self.media.get_meta(vlc.Meta.Title))
#
#         #self.mediaplayer.set_hwnd(int(self.videoframe.winId()))
#
