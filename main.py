import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen
from dunwoody_disaster.views.CharacterSelector import CharacterSelector
from dunwoody_disaster.CharacterFactory import CharacterFactory, Character


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: #2f2f2f;")
        self.player = None
        dimensions = QApplication.primaryScreen().size()
        self.setMaximumWidth(dimensions.width())
        self.setMaximumHeight(dimensions.height())

        player1 = CharacterFactory.createTestChar()
        player2 = CharacterFactory.createTestChar()
        playable_characters = [player1]

        self.startMenu = StartMenu()
        self.startMenu.onStart(self.startBtnClicked)

        self.selector = CharacterSelector(playable_characters)
        self.selector.onSelect(self.userSelectedCharacter)

        self.fightScreen = FightScreen(player1, player2)

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.selector)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentWidget(self.mapScreen)

    def EnterFight(self):
        """
        Enter fight screen by pointing stack at fight screen.
        This will need to be changed to set the proper opponent per setting. Index 2 is the fight screen.
        """
        self.stack.removeWidget(self.fightScreen)
        self.fightScreen.player1 = self.player

        print("entering fight")
        player2 = CharacterFactory.createTestChar()
        self.fightScreen = FightScreen(self.player, player2)
        self.stack.addWidget(self.fightScreen)
        self.fightScreen.init_UI()
        self.stack.setCurrentWidget(self.fightScreen)

    def startBtnClicked(self):
        self.stack.setCurrentWidget(self.selector)

    def userSelectedCharacter(self, character: Character):
        self.player = character
        self.mapScreen = MapScreen.build_map(self.player)
        self.mapScreen.onEnter(self.EnterFight)
        self.stack.addWidget(self.mapScreen)
        self.showMapScreen()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
