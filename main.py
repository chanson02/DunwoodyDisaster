import sys
import pygame
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen, Map
from dunwoody_disaster.views.crawlScreen import Crawl
from dunwoody_disaster.views.CharacterSelector import CharacterSelector
from dunwoody_disaster.CharacterFactory import CharacterFactory, Character
from dunwoody_disaster.views.defeatScreen import DefeatScreen
from dunwoody_disaster.views.victoryScreen import VictoryScreen
from dunwoody_disaster.views.dialogueScreen import DialogueScreen
from dunwoody_disaster import AUDIO


# test
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: black; color: #FFFFFF;")
        self.setupMusicPlayer()
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

    def setupMusicPlayer(self):
        # Initialize Pygame mixer
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(AUDIO["TitleScreenMusic"])
        pygame.mixer.music.set_volume(1.0)  # Set volume from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # Play indefinitely
        self.Fire_Sound1 = pygame.mixer.Sound(AUDIO["FireCrackle"])
        self.Fire_Sound1.set_volume(0.1)
        self.Fire_Sound1.play(loops=-1)

    def startBtnClicked(self):
        pygame.mixer.music.stop()
        self.Fire_Sound1.stop()
        pygame.mixer.music.load(AUDIO["CrawlMusic"])
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1)

        self.crawl = Crawl()
        self.crawl.onFinish(self.showSelector)
        self.stack.addWidget(self.crawl)
        self.stack.setCurrentWidget(self.crawl)

    def showSelector(self):
        pygame.mixer.music.stop()
        self.stack.setCurrentWidget(self.selector)

    def createPlayableCharacters(self) -> list[Character]:
        return [
            CharacterFactory.Cooper(),
            CharacterFactory.Mitch(),
            CharacterFactory.Noah(),
            CharacterFactory.John(),
        ]

    def userSelectedCharacter(self, character: Character):
        self.player = character
        self.saveCharacter(character)
        self.mapScreen = MapScreen(Map.buildMap(self.player))
        self.mapScreen.setStyleSheet("background-color: #41A392;")
        self.mapScreen.onEnter(self.EnterFight)
        self.stack.addWidget(self.mapScreen)
        self.showMapScreen()

    def showMapScreen(self):
        pygame.mixer.music.stop()
        self.mapScreen.map.setRoom(None)
        unbeaten = self.mapScreen.map.unbeaten_rooms()
        if len(unbeaten) > 0:
            self.mapScreen.map.setRoom(unbeaten[0])
        self.stack.setCurrentWidget(self.mapScreen)

    def showDialogue(
        self, char1: Character, char2: Character, dialogues_char1, dialogues_char2
    ):
        if self.dialogueScreen is not None:
            self.stack.removeWidget(self.dialogueScreen)

        self.dialogueScreen = DialogueScreen(char1, char2)
        self.dialogueScreen.set_dialogue(dialogues_char1, dialogues_char2)
        self.dialogueScreen.onComplete(self.onDialogueComplete)
        self.stack.addWidget(self.dialogueScreen)
        self.stack.setCurrentWidget(self.dialogueScreen)

    def onDialogueComplete(self):
        print("Dialogue completed!")
        # Here you can add what happens after the dialogue is complete.
        self.showMapScreen()  # Example: Return to the map screen.

    def EnterFight(self, room: dict):
        """
        Enter fight screen by pointing stack at fight screen.
        This will need to be changed to set the proper opponent per setting. Index 2 is the fight screen.
        """
        if not self.player:
            raise Exception("Cannot enter fight when no player is selected")

        if self.fight:
            self.stack.removeWidget(self.fight.widget)

        self.fight = FightSequence(self.player, room["NPC"], room["battlefield"])
        self.fight.onWin(self.showVictoryScreen)
        self.fight.onLose(self.showDefeatScreen)

        self.stack.addWidget(self.fight.widget)
        self.fight.widget.animation_Object.start()
        self.stack.setCurrentWidget(self.fight.widget)

    def saveCharacter(self, character: Character):
        CharacterFactory.SaveCharacter(character)

    def loadCharacter(self, name: str) -> Character:
        return CharacterFactory.LoadCharacter(name)

    def showVictoryScreen(self):
        if self.fight is None:
            raise Exception("Victory Screen expects a fight")

        victory = VictoryScreen(self.fight)

        def loot_collected():
            self.stack.removeWidget(victory)
            self.showMapScreen()
            self.saveCharacter(self.player)

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

        """     def closeEvent(self, event):
        _ = event  # silence unused warning
        self.fight.widget.animation_Object.stop() """


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())
