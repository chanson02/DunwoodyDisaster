import sys
import pygame
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster.views.BattleSimulation import Game


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: #2f2f2f;")
        self.setMinimumSize(800, 600)

        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()

        self.startMenu = StartMenu()
        self.startMenu.onStart(self.showMapScreen)

        self.mapScreen = MapScreen.build_map(player1)
        self.fightScreen = FightScreen(player1, player2)

        self.mapScreen.battle_start.connect(self.start_pygame_battle)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentWidget(self.mapScreen)
        print("passed")

    def start_pygame_battle(self):
        # self.hide()  # hide the main window
        battle_game = Game(self)
        battle_game.run()
        self.show()  # Show the main window

    def test_update_pyside(self, bites: bytes):
        from PySide6.QtGui import QPixmap, QImage
        # imgimg = QImage(data=bites, width=400, height=300, format=QImage.Format.Format_RGB16)
        # # QImage(self, data: Union\[bytes, bytearray, memoryview\], width: int, height: int, bytesPerLine: int, format: PySide6.QtGui.QImage.Format, cleanupFunction: Optional\[Callable\] = None, cleanupInfo: Optional\[int\] = None) -> None
        # img = QPixmap.fromImage(imgimg)
        # self.mapScreen.map.setPixmap(img)

        img = QImage(bites, 800, 600, QImage.Format.Format_RGB888)
        #img = QImage(bites, 800, 600, QImage.Format.Format_ARGB32)
        pixmap = QPixmap.fromImage(img)
        self.mapScreen.map.setPixmap(pixmap)
        print('this ran')


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
