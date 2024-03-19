from PySide6 import QtCore
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QScrollArea, QLabel, QVBoxLayout, QGridLayout, QFrame, QSizePolicy, QHBoxLayout

from libertv.tiles.back import BackTile
from libertv.tiles.category import CategoryTile
from libertv.collector_tile import CollectorTile
from libertv.db import LiberDB
from libertv.item_tile import ItemTile


class ListPanel(QWidget):

    tiles = None
    current_tile_idx = None

    tiles_in_row = None

    parent_id = None
    parent_type = None
    parent_parent_id = None
    parent_parent_type = None

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

        # self._widget = QWidget()

        self._rows = QVBoxLayout()
        self.flow_keeper = QWidget()

        self.fill_panel(self.get_tiles())
        # self._widget.setLayout(self._rows)

        self._scroll_area = QScrollArea()
        self._scroll_position = 0
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        #self.flow_keeper.setStyleSheet("QWidget {border: 2px solid #ff0000;}")
        self.flow_keeper.setSizePolicy(sizePolicy)
        self.flow_keeper.setLayout(self._rows)
        self._scroll_area.setWidget(self.flow_keeper)
        self._scroll_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self._scroll_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        self._vbox.addWidget(self._scroll_area)

        self.setLayout(self._vbox)

    tile_height = 150

    def get_back_tile(self, parent_id=None, parent_type=None):
        size = self.screen().availableGeometry().size()
        back = BackTile(f"Back", size)
        back.tid = parent_id
        back.type = parent_type
        back.setStyleSheet(self.css_normal_tile)
        back.setProperty("class", "tile_collector")
        back.setMaximumWidth(size.width() // self.tiles_in_row - 20)
        back.setMinimumWidth(size.width() // self.tiles_in_row - 20)
        back.setMaximumHeight(self.tile_height)
        back.setMinimumHeight(self.tile_height)
        return back

    def get_tiles(self, parent=None):
        size = self.screen().availableGeometry().size()

        tiles = []

        if self.parent_id:
            parent_item = self.db.get_parent(parent_id=self.parent_id, parent_type=self.parent_type)
            tiles.append(self.get_back_tile(parent_item["parent_id"], self.parent_type))
            self._title_label.setText(parent_item["name"])
        else:
            self._title_label.setText("Liber TV")

        category_tiles = self.db.get_categories(parent_id=self.parent_id)
        for tile in category_tiles:
            category = CategoryTile(f"{tile['name']}", size)
            category.tid = tile['id']
            category.type = "category"
            category.setStyleSheet(self.css_normal_category_tile)
            category.setMaximumWidth(size.width() // self.tiles_in_row - 20)
            category.setMinimumWidth(size.width() // self.tiles_in_row - 20)
            category.setMaximumHeight(self.tile_height)
            category.setMinimumHeight(self.tile_height)
            tiles.append(category)

        return tiles

    def insert_label(self, j):
        size = self.screen().availableGeometry().size()

        label = QLabel(f"Col {j}")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet(self.css_normal_category_tile)
        label.setMaximumWidth(size.width() // self.tiles_in_row - 20)
        label.setMinimumWidth(size.width() // self.tiles_in_row - 20)
        label.setMaximumHeight(self.tile_height)
        label.setMinimumHeight(self.tile_height)
        return label

    def fill_in_row(self, tiles):
        widget = QWidget()
        # widget.setStyleSheet("QWidget {border: 2px solid #00ff00;}")

        cols = QHBoxLayout()
        for item in tiles:
            cols.addWidget(item)
            self.tiles.append(item)
        widget.setLayout(cols)

        return widget

    def fill_panel(self, items):
        size = self.screen().availableGeometry().size()

        self.empty_panel()
        self.tiles = []
        rows_count = 0
        current_row = None
        for tile in self.get_tiles():
            if rows_count == 0 or rows_count % 6 == 0:
                widget = QWidget()
                current_row = QHBoxLayout()
                widget.setLayout(current_row)
                widget.setFixedWidth(size.width()-50)
                self._rows.addWidget(widget)
            if current_row:
                current_row.addWidget(tile, 0, Qt.Alignment.AlignLeft)
                self.tiles.append(tile)
            rows_count += 1
        if rows_count % 6 != 0:
            current_row.addStretch()
        self.flow_keeper.setFixedHeight((self.tile_height + 20) * self._rows.count())
        self.set_current_tile()

    def empty_panel(self):
        self.current_tile_idx = 0
        for i in reversed(range(self._rows.count())):
            for j in reversed(self._rows.itemAt(i).widget().children()):
                j.deleteLater()
            self._rows.itemAt(i).widget().deleteLater()
            self._rows.removeItem(self._rows.itemAt(i))

    def go_p(self):
        self.fill_panel(2)

    # def add_tiles(self):
    #     size = self.screen().availableGeometry().size()
    #
    #     # remove children first
    #     while (child := self._flow_layout.takeAt(0)) != None:
    #         child.widget().hide()
    #         child.widget().setParent(None)
    #         self._flow_layout.removeWidget(child.widget())
    #
    #     self.tiles = []
    #     self.current_tile_idx = 0
    #
    #     counter = 0
    #     row = 0
    #     col = 0
    #
    #     if self.parent_id:  # TODO: give it a real condition
    #         back = BackTile(f"Back")
    #         back.tid = self.parent_parent_id
    #         back.type = self.parent_parent_type
    #         back.setStyleSheet(self.css_normal_tile)
    #         back.setProperty("class", "tile_collector")
    #         back.setMinimumWidth(100)
    #         back.setMinimumHeight(200)
    #         self.tiles.append(back)
    #         back.show()
    #         self._flow_layout.addWidget(back, row, col)
    #
    #         counter += 1
    #         col += 1
    #
    #     category_tiles = self.db.get_categories(parent_id=self.parent_id)
    #     for tile in category_tiles:  # 10 times is just for now
    #         category = CategoryTile(f"{tile['name']}", size)
    #         category.tid = tile['id']
    #         category.type = "category"
    #         category.setStyleSheet(self.css_normal_category_tile)
    #         category.setMinimumWidth(size.width()//self.tiles_in_row-30)
    #         category.setMinimumHeight(150)
    #         self.tiles.append(category)
    #         category.show()
    #         self._flow_layout.addWidget(category, row, col)
    #
    #         counter += 1
    #         col += 1
    #         if counter % self.tiles_in_row == 0:
    #             row += 1
    #             col = 0
    #
    #     series_tiles = self.db.get_series(parent_id=self.parent_id)
    #     for tile in series_tiles:
    #         collector = CollectorTile(f"{tile['name']}")
    #         collector.setStyleSheet(self.css_normal_tile)
    #         collector.setProperty("class", "tile_collector")
    #         collector.setMinimumWidth(100)
    #         collector.setMinimumHeight(200)
    #         self.tiles.append(collector)
    #         self._flow_layout.addWidget(collector, row, col)
    #
    #         counter += 1
    #         col += 1
    #         if counter % self.tiles_in_row == 0:
    #             row += 1
    #             col = 0
    #
    #     item_tiles = self.db.get_items(category_id=self.parent_id)
    #     for tile in item_tiles:
    #         item = ItemTile(f"{tile['name']}")
    #         item.setStyleSheet(self.css_normal_tile)
    #         item.setProperty("class", "tile_collector")
    #         item.setMinimumWidth(100)
    #         item.setMinimumHeight(200)
    #         self.tiles.append(item)
    #         self._flow_layout.addWidget(item, row, col)
    #
    #         counter += 1
    #         col += 1
    #         if counter % self.tiles_in_row == 0:
    #             row += 1
    #             col = 0
    #     self.set_current_tile()

    def move_scroll(self, up=False):
        size = self._scroll_area.screen().availableGeometry().size()
        scroll_position = self._scroll_area.verticalScrollBar().value()
        tile_height = self.tiles[self.current_tile_idx].height()
        tile_y = self.tiles[self.current_tile_idx].parent().y()
        if up and scroll_position > tile_y:
            self._scroll_area.verticalScrollBar().setValue(scroll_position - tile_height)
        elif not up and size.height() < tile_y + tile_height:
            self._scroll_area.verticalScrollBar().setValue(scroll_position + tile_height)

    def reset_tiles(self):
        for tile in self.tiles:
            tile.setStyleSheet(self.css_normal_category_tile)

    def set_current_tile(self):
        if self.tiles:
            self.tiles[self.current_tile_idx].setStyleSheet(self.css_selected_category_tile)

    def go_enter_key(self):
        self.parent_parent_id = self.parent_id
        self.parent_parent_type = self.parent_type
        self.parent_id = self.tiles[self.current_tile_idx].tid
        self.parent_type = self.tiles[self.current_tile_idx].type
        # print(f"parent parent: {self.parent_parent_id} ({self.parent_parent_type})")
        # print(f"parent: {self.parent_id} ({self.parent_type})")
        self.fill_panel(self.get_tiles())

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
        self.reset_tiles()
        if self.current_tile_idx + self.tiles_in_row < len(self.tiles):
            self.current_tile_idx += self.tiles_in_row
        self.set_current_tile()
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
