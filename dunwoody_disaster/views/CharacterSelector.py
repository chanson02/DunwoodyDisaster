from typing import Callable
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD


class CharacterSelector(QWidget):
    def __init__(self, characters: list[Character]):
        super().__init__()
        self.selected = None
        self._callback = DD.unimplemented
        self.setStyleSheet("background-color: #2f2f2f;")

        row = 0

        layout = QGridLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        layout.addItem(DD.expander(True, True, 50))
        row += 1

        titleLayout = QGridLayout()
        titleLayout.setSpacing(0)
        titleLayout.setContentsMargins(0, 0, 0, 0)
        titleLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 0
        )
        lbl = QLabel("Choose your champion")
        lbl.setStyleSheet(
            'background-color: black; font-size: 36px; font-weight: 600; font-family: "Futura Bk BT";'
        )
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titleLayout.addWidget(lbl, 0, 1)
        titleLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 2
        )
        layout.addLayout(titleLayout, row, 1)
        row += 1

        layout.addItem(QSpacerItem(0, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)
        row += 1

        container = QWidget()
        container.setStyleSheet("min-width: 0px;")
        hbox = QHBoxLayout()
        for character in characters:
            hbox.addWidget(self.characterWidget(character))
        container.setLayout(hbox)
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("min-width: 800px;")
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        layout.addWidget(scroll_area, row, 1)
        row += 1

        layout.addItem(QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)
        row += 1

        btnLayout = QGridLayout()
        btnLayout.setSpacing(0)
        btnLayout.setContentsMargins(0, 0, 0, 0)
        btnLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 0
        )
        self.select_lbl = QLabel("Selected: None")
        self.select_lbl.setStyleSheet(
            'background-color: black; font-size: 24px; font-weight: 600; font-family: "Futura Bk BT"'
        )
        self.select_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btnLayout.addWidget(self.select_lbl, 0, 1)
        btnLayout.addItem(
            QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), 1, 0
        )
        btn = QPushButton("Confirm")
        btn.setStyleSheet(
            "background-color: gray; min-width: 250px; font-size: 14px; font-weight: 600px;"
        )
        btn.clicked.connect(self.confirm)
        btnLayout.addWidget(btn, 2, 1)
        btnLayout.addItem(
            QSpacerItem(0, 0, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 0, 2
        )
        layout.addLayout(btnLayout, row, 1)
        row += 1

        layout.addItem(
            QSpacerItem(
                50, 50, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            row,
            2,
        )
        row += 1

    def characterWidget(self, char: Character) -> QWidget:
        layout = QVBoxLayout()
        lbl = QLabel(char.name)
        lbl.setStyleSheet(
            'background-color: black; font-size: 20px; font-family: "Futura Bk BT"'
        )
        layout.addWidget(lbl)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        img = QLabel()
        img.setPixmap(char.image().scaledToWidth(250))
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img.setStyleSheet("background-color: white;")
        layout.addWidget(img)

        widget = QWidget()
        widget.setStyleSheet("background-color: black;")
        widget.setLayout(layout)
        DD.clickable(widget).connect(self.lambda_select(char))
        return widget

    def onSelect(self, callback: Callable):
        """
        :param callback: A function that takes a Character as a parameter
        """
        self._callback = callback

    def confirm(self):
        if not self.selected:
            return

        self._callback(self.selected)

    def lambda_select(self, char: Character):
        return lambda: self.select(char)

    def select(self, char: Character):
        self.selected = char
        self.select_lbl.setText(f"Selected: {char.name}")
