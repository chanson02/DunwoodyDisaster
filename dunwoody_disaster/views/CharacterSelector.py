from typing import Callable
from PySide6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton, QScrollArea
from PySide6.QtCore import Qt
from dunwoody_disaster.CharacterFactory import Character
import dunwoody_disaster as DD


class CharacterSelector(QWidget):
    def __init__(self, characters: list[Character]):
        super().__init__()
        self.selected = None
        self._callback = DD.unimplemented
        layout = QVBoxLayout()
        self.setLayout(layout)

        lbl = QLabel("Choose your champion")
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        scroll_area = QScrollArea()
        container = QWidget()
        hbox = QHBoxLayout()
        for character in characters:
            hbox.addWidget(self.characterWidget(character))

        layout.addWidget(scroll_area)
        scroll_area.setWidget(container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        container.setLayout(hbox)

        self.select_lbl = QLabel("Selected: None")
        layout.addWidget(self.select_lbl)

        btn = QPushButton("Confirm")
        btn.clicked.connect(self.confirm)
        layout.addWidget(btn)

    def characterWidget(self, char: Character) -> QWidget:
        layout = QVBoxLayout()
        lbl = QLabel(char.name)
        layout.addWidget(lbl)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)

        img = QLabel()
        img.setPixmap(char.image().scaledToWidth(300))
        img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(img)

        widget = QWidget()
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
