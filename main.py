import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen, Map
from dunwoody_disaster.views.crawlScreen import Crawl
from dunwoody_disaster.views.CharacterSelector import CharacterSelector
from dunwoody_disaster.CharacterFactory import CharacterFactory, Character

from dunwoody_disaster.views.defeatScreen import DefeatScreen
from dunwoody_disaster.views.victoryScreen import VictoryScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: black; color: #FFFFFF;")
        self.player = None

        self.startMenu = StartMenu()
        self.startMenu.onStart(self.startBtnClicked)

        self.selector = CharacterSelector(self.createPlayableCharacters())
        self.selector.onSelect(self.userSelectedCharacter)
        self.fight = None

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.selector)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.mapScreen.map.setRoom(None)
        self.stack.setCurrentWidget(self.mapScreen)

    def EnterFight(self, room: dict):
        """
        Enter fight screen by pointing stack at fight screen.
        This will need to be changed to set the proper opponent per setting. Index 2 is the fight screen.
        """
        if not self.player:
            raise Exception("Cannot enter fight when no player is selected")

        if self.fight:
            self.stack.removeWidget(self.fight.widget)

        self.fight = FightSequence(self.player, room["NPC"])
        self.fight.onWin(self.showVictoryScreen)
        self.fight.onLose(self.showDefeatScreen)

        self.stack.addWidget(self.fight.widget)
        self.fight.widget.animation_Object.start()
        self.stack.setCurrentWidget(self.fight.widget)

    def startBtnClicked(self):
        self.crawl = Crawl()
        self.crawl.onFinish(self.showSelector)
        self.stack.addWidget(self.crawl)
        self.stack.setCurrentWidget(self.crawl)

    def showSelector(self):
        self.stack.setCurrentWidget(self.selector)

    def userSelectedCharacter(self, character: Character):
        self.player = character
        self.mapScreen = MapScreen(Map.buildMap(self.player))
        self.mapScreen.setStyleSheet("background-color: #41A392;")
        self.mapScreen.onEnter(self.EnterFight)
        self.stack.addWidget(self.mapScreen)
        self.showMapScreen()

    def createPlayableCharacters(self) -> list[Character]:
        # cooper = CharacterFactory.Cooper()
        return [
            CharacterFactory.Cooper(),
            CharacterFactory.Mitch(),
            CharacterFactory.Noah(),
            CharacterFactory.John(),
        ]

    def showVictoryScreen(self):
        if self.fight is None:
            raise Exception("Victory Screen expects a fight")

        victory = VictoryScreen(self.fight)

        def loot_collected():
            self.stack.removeWidget(victory)
            self.showMapScreen()

        victory.onClose(loot_collected)
        self.stack.addWidget(victory)
        self.fight.widget.animation_Object.stop()
        self.stack.setCurrentWidget(victory)

    def showDefeatScreen(self):
        if self.fight is None:
            raise Exception("Defeat Screen expects a fight")

        defeat = DefeatScreen()

        def return_to_map():
            self.stack.removeWidget(defeat)
            self.showMapScreen()

        defeat.onClose(return_to_map)
        self.stack.addWidget(defeat)
        self.fight.widget.animation_Object.stop()
        self.stack.setCurrentWidget(defeat)

    def closeEvent(self, event):
        _ = event  # silence unused warning
        self.fight.widget.animation_Object.stop()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())
