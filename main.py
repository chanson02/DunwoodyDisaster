import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: #2f2f2f;")

        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()

        self.startMenu = StartMenu()
        self.startMenu.onStart(self.showMapScreen)

        self.mapScreen = MapScreen.build_map(player1)
        self.fightScreen = FightScreen(player1, player2)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentWidget(self.mapScreen)
        print("passed")


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
