from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QGridLayout, QFrame, QSizePolicy

from libertv.back_tile import BackTile
from libertv.category_tile import CategoryTile
from libertv.collector_tile import CollectorTile
from libertv.db import LiberDB
from libertv.item_tile import ItemTile
from libertv.toolbox.flow_layout import FlowLayout


class ListPanel(QWidget):

    tiles = None
    current_tile_idx = None

    tiles_in_row = None

    parent_id = None
    parent_tile = None
    parent_parent_tile = None

    css_normal_tile = "QWidget {font-size: 18px; padding-bottom: 10px; border-radius: 20px;}"
    css_normal_category_tile = "QWidget {font-size: 18px; padding-bottom: 10px; border-radius: 20px;}"
    css_selected_tile = "QWidget {font-size: 23px; padding-bottom: 10px; border-radius: 20px;}"

    def __init__(self):
        super().__init__()

        self.db = LiberDB()
        self.tiles = []
        self.current_tile_idx = 0
        self.tiles_in_row = 6

        self.setWindowTitle("Category selection")

        self._vbox = QVBoxLayout()
        self._title_label = QLabel("Liber TV")
        self._title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        self._vbox.addWidget(self._title_label)

        self._flow_layout = QGridLayout()
        self.add_tiles()


        self._scroll_area = QScrollArea()
        self._scroll_position = 0
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self._scroll_area.sizePolicy().hasHeightForWidth())
        flow_keeper = QWidget()
        flow_keeper.setSizePolicy(sizePolicy)
        flow_keeper.setLayout(self._flow_layout)
        self._scroll_area.setWidget(flow_keeper)

        self._vbox.addWidget(self._scroll_area)

        self.setLayout(self._vbox)

    def add_tiles(self):

        self.tiles = []
        self.current_tile_idx = 0

        for child in self._flow_layout.children():
            self._flow_layout.removeWidget(child)

        counter = 0
        row = 0
        col = 0

        if self.parent_id:  # TODO: give it a real condition
            back = BackTile(f"Back")
            back.setStyleSheet(self.css_normal_tile)
            back.setProperty("class", "tile_collector")
            back.setMinimumWidth(100)
            back.setMinimumHeight(200)
            self.tiles.append(back)
            self._flow_layout.addWidget(back, row, col)

            counter += 1
            col += 1

        category_tiles = self.db.get_categories(parent_id=self.parent_id)
        for tile in category_tiles*10:
            category = CategoryTile(f"{tile['name']}")
            category.setStyleSheet("QWidget {border: 1px solid #990000;height: 300px;}")
            #category.setStyleSheet(self.css_normal_tile)
            #category.setProperty("class", "tile_category")
            category.setMinimumWidth(128)
            category.setMinimumHeight(100)
            self.tiles.append(category)
            self._flow_layout.addWidget(category, row, col)

            counter += 1
            col += 1
            if counter % 6 == 0:
                row += 1
                col = 0

        series_tiles = self.db.get_series(parent_id=self.parent_id)
        for tile in series_tiles:
            collector = CollectorTile(f"{tile['name']}")
            collector.setStyleSheet(self.css_normal_tile)
            collector.setProperty("class", "tile_collector")
            collector.setMinimumWidth(100)
            collector.setMinimumHeight(200)
            self.tiles.append(collector)
            self._flow_layout.addWidget(collector, row, col)

            counter += 1
            col += 1
            if counter % 6 == 0:
                row += 1
                col = 0

        item_tiles = self.db.get_items(category_id=self.parent_id)
        for tile in item_tiles:
            item = ItemTile(f"{tile['name']}")
            item.setStyleSheet(self.css_normal_tile)
            item.setProperty("class", "tile_collector")
            item.setMinimumWidth(100)
            item.setMinimumHeight(200)
            self.tiles.append(item)
            self._flow_layout.addWidget(item, row, col)

            counter += 1
            col += 1
            if counter % 6 == 0:
                row += 1
                col = 0
        self.set_current_tile()

    def reset_tiles(self):
        for tile in self.tiles:
            tile.setStyleSheet(self.css_normal_tile)

    def set_current_tile(self):
        self.tiles[self.current_tile_idx].setStyleSheet(self.css_selected_tile)

    def go_enter_key(self):
        self.add_tiles()

    def go_right(self):
        if self.current_tile_idx < len(self.tiles) - 1:
            self.current_tile_idx += 1
        else:
            self.current_tile_idx = len(self.tiles) - 1
        self.reset_tiles()
        self.set_current_tile()

    def go_left(self):
        if self.current_tile_idx > 0:
            self.current_tile_idx -= 1
        else:
            self.current_tile_idx = 0
        self.reset_tiles()
        self.set_current_tile()

    def go_down(self):
        if self.current_tile_idx + self.tiles_in_row < len(self.tiles):
            self.current_tile_idx += self.tiles_in_row
        self.reset_tiles()
        self.set_current_tile()
        # TODO: get position by real position of scrolled area
        pixels = 105
        if self._scroll_position > 0:
            pass
        self._scroll_position += pixels
        self._scroll_area.scroll(0, pixels)

    def go_shift_down(self):
        if self.current_tile_idx + self.tiles_in_row*10 < len(self.tiles):
            self.current_tile_idx += self.tiles_in_row*10
        self.reset_tiles()
        self.set_current_tile()
        # TODO: get position by real position of scrolled area
        pixels = 105
        if self._scroll_position > 0:
            pass
        self._scroll_position += pixels
        self._scroll_area.scroll(0, pixels)

    def go_up(self):
        if self.current_tile_idx - self.tiles_in_row >= 0:
            self.current_tile_idx -= self.tiles_in_row
        self.reset_tiles()
        self.set_current_tile()
        # TODO: get position by real position of scrolled area
        pixels = -105
        if self._scroll_position < 0:
            self._scroll_area.scroll(0, self._scroll_position)
            self._scroll_position = 0
        else:
            self._scroll_position -= pixels
            self._scroll_area.scroll(0, pixels)

    def go_shift_up(self):
        if self.current_tile_idx - self.tiles_in_row*10 >= 0:
            self.current_tile_idx -= self.tiles_in_row*10
        self.reset_tiles()
        self.set_current_tile()
        # TODO: get position by real position of scrolled area
        pixels = -105
        if self._scroll_position < 0:
            self._scroll_area.scroll(0, self._scroll_position)
            self._scroll_position = 0
        else:
            self._scroll_position -= pixels
            self._scroll_area.scroll(0, pixels)
