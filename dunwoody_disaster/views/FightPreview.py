from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QPainter
from dunwoody_disaster.CharacterFactory import Character

class FightPreview(QWidget):
    #def __init__(self, name: str, character: Character, battlefield: str):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.room_lbl = QLabel()
        layout.addWidget(self.room_lbl)

        self.battlefield = QLabel()
        layout.addWidget(self.battlefield)



    def set_room(self, room_info: dict):
        NPC = room_info['NPC']
        lbl = f"{room_info['name']}: {NPC.name}"
        self.room_lbl.setText(lbl)

        bkg = QPixmap(room_info['battlefield']).scaledToWidth(400)
        self.battlefield.setPixmap(self.center_overlay(bkg, NPC.image().scaledToWidth(50)))



    def center_overlay(self, background: QPixmap, foreground: QPixmap) -> QPixmap:
        x = (background.width() - foreground.width()) // 2
        y = (background.height() - foreground.height()) // 2
        painter = QPainter(background)
        painter.drawPixmap(x, y, foreground)
        painter.end()
        return background
