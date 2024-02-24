from PySide6 import QtCore
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QGridLayout, QFrame, QSizePolicy

from libertv.back_tile import BackTile
from libertv.tiles.category import CategoryTile
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
    css_normal_category_tile = (
        "QWidget {border: 1px solid #1b263b; font-size: 18px; "
        "padding: 10px 20px; border-radius: 20px; "
        "background-color: #415a77; color: #e0e1dd;}"
    )
    css_selected_category_tile = (
        "QWidget {border: 1px solid #4A8D7C; font-size: 18px; "
        "padding: 10px 20px; border-radius: 20px; font-weight: bold;"
        "background-color: #A4CBC1; color: #27705E;}"
    )

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
        flow_keeper = QWidget()
        flow_keeper.setSizePolicy(sizePolicy)
        flow_keeper.setLayout(self._flow_layout)
        self._scroll_area.setWidget(flow_keeper)
        self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._vbox.addWidget(self._scroll_area)

        self.setLayout(self._vbox)

    def add_tiles(self):
        size = self.screen().availableGeometry().size()

        self.tiles = []
        self.current_tile_idx = 0

        # remove children first
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
        for tile in category_tiles*30:  # 10 times is just for now
            category = CategoryTile(f"{tile['name']}", size)
            category.tid = tile['id']
            category.type = "category"
            category.setStyleSheet(self.css_normal_category_tile)
            #category.setStyleSheet(self.css_normal_tile)
            #category.setProperty("class", "tile_category")
            category.setMinimumWidth(size.width()//6-30)
            category.setMinimumHeight(150)
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

    def move_scroll(self, up=False):
        print("AAA")
        size = self._scroll_area.screen().availableGeometry().size()
        scroll_position = self._scroll_area.verticalScrollBar().value()
        tile_height = self.tiles[self.current_tile_idx].height()
        tile_y = self.tiles[self.current_tile_idx].y()
        print(size)
        print(self.tiles[self.current_tile_idx].y(), ':', self.tiles[self.current_tile_idx].height())
        if up and scroll_position > tile_y:
            self._scroll_area.verticalScrollBar().setValue(scroll_position - tile_height)
        elif not up and size.height() < tile_y + tile_height:
            self._scroll_area.verticalScrollBar().setValue(scroll_position + tile_height)

    def reset_tiles(self):
        for tile in self.tiles:
            tile.setStyleSheet(self.css_normal_category_tile)

    def set_current_tile(self):
        self.tiles[self.current_tile_idx].setStyleSheet(self.css_selected_category_tile)

    def go_enter_key(self):
        self.parent_id = self.tiles[self.current_tile_idx].tid
        self.parent_type = self.tiles[self.current_tile_idx].type
        self.add_tiles()

    def go_right(self):
        if self.current_tile_idx < len(self.tiles) - 1:
            self.current_tile_idx += 1
        else:
            self.current_tile_idx = len(self.tiles) - 1
        self.reset_tiles()
        self.set_current_tile()
        self.move_scroll()

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
        self.move_scroll()

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
        self.move_scroll(True)

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
