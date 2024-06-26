import sys
import pygame
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeyEvent
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.FightSequence import FightSequence
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen, Map
from dunwoody_disaster.views.crawlScreen import Crawl
from dunwoody_disaster.views.creditScreen import Credits
from dunwoody_disaster.views.CharacterSelector import CharacterSelector
from dunwoody_disaster.CharacterFactory import CharacterFactory, Character
from dunwoody_disaster.views.defeatScreen import DefeatScreen
from dunwoody_disaster.views.victoryScreen import VictoryScreen
from dunwoody_disaster.views.dialogueScreen import DialogueScreen

# from dunwoody_disaster.views.CharacterDetailWidget import CharacterDetailWidget
from dunwoody_disaster.views.MonologueWidget import (
    MonologueWidget,
)
from dunwoody_disaster.EventIdentifier import EventIdentifier

from dunwoody_disaster import AUDIO
from dunwoody_disaster.views.introductions.Cooper import CooperIntroScreen
from dunwoody_disaster.views.introductions.Noah import NoahIntroScreen
from dunwoody_disaster.views.introductions.Mitch import MitchIntroScreen
from dunwoody_disaster.views.introductions.John import JohnIntroScreen

default_font = QFont("blood crow", 12)  # Font family is Arial and font size is 12
QApplication.setFont(default_font)


def should_display_monologue(player, opponent):
    # Placeholder for logic to determine if a monologue should be displayed
    return opponent.name


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        self.setStyleSheet("background-color: black; color: #FFFFFF;")
        self.currentScreen = None  # To keep track of the current screen
        self.player = None
        self.fight = None
        self.stack = QStackedWidget()
        self.startMenu = StartMenu()
        self.startMenu.onStart(self.startBtnClicked)

        self.setCentralWidget(self.stack)
        self.stack.addWidget(self.startMenu)
        self.showStartMenu()

    def showStartMenu(self):
        self.startMenu.movie.start()
        self.stack.setCurrentWidget(self.startMenu)
        self.setupMusicPlayer()

    def setupMusicPlayer(self):
        # Initialize Pygame mixer
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(AUDIO["TitleScreenMusic"])
        pygame.mixer.music.set_volume(1.0)  # Set volume from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # Play indefinitely
        # Load and play fire crackle sound; only set sounds to variables and not music.
        self.Fire_Sound1 = pygame.mixer.Sound(AUDIO["FireCrackle"])
        self.Fire_Sound1.set_volume(0.05)
        self.Fire_Sound1.play(loops=-1)
        # Load and play wind sound
        self.Wind_Sound = pygame.mixer.Sound(AUDIO["Wind"])
        self.Wind_Sound.set_volume(0.05)
        self.Wind_Sound.play(loops=-1)

    def startBtnClicked(self):
        pygame.mixer.music.stop()
        self.Fire_Sound1.stop()
        self.Wind_Sound.stop()
        pygame.mixer.music.load(AUDIO["CrawlMusic"])
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play()

        self.crawl = Crawl()
        self.crawl.onFinish(self.showSelector)
        self.stack.addWidget(self.crawl)
        self.stack.setCurrentWidget(self.crawl)

    def showSelector(self):
        self.selector = CharacterSelector(CharacterFactory.playable())
        self.selector.onSelect(self.userSelectedCharacter)
        self.stack.addWidget(self.selector)
        pygame.mixer.music.stop()
        pygame.mixer.music.load(AUDIO["CharacterSelectionMusic"])
        pygame.mixer.music.set_volume(1.0)  # Set volume from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # Play indefinitely
        self.stack.setCurrentWidget(self.selector)

    def userSelectedCharacter(self, character: Character):
        self.player = character
        self.saveCharacter(character)
        self.displayCharacterDetails(character)
        self.mapScreen = MapScreen(Map.buildMap(self.player))
        self.mapScreen.setStyleSheet("background-color: #41A392;")
        self.mapScreen.onEnter(self.playDialogue)
        self.stack.addWidget(self.mapScreen)

    def stopAllSounds(self):
        pygame.mixer.music.stop()  # Stop the music that is currently playing

    def displayCharacterDetails(self, character):
        self.stopAllSounds()
        if character.name == "John":
            # Load John's theme music
            pygame.mixer.music.load(AUDIO["JohnTheme"])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

            self.characterWidget = JohnIntroScreen(
                character, transition_callback=self.showMapScreen
            )
        elif character.name == "Cooper":
            self.characterWidget = CooperIntroScreen(
                character, transition_callback=self.showMapScreen
            )
        elif character.name == "Mitch":
            # Load Mitch's theme music
            pygame.mixer.music.load(AUDIO["MitchTheme"])
            # Set the volume to maximum (1.0)
            pygame.mixer.music.set_volume(1.0)
            # Play John's theme music in a loop indefinitely
            pygame.mixer.music.play(-1)

            self.characterWidget = MitchIntroScreen(
                character, transition_callback=self.showMapScreen
            )
        elif character.name == "Noah":
            pygame.mixer.music.load(AUDIO["NoahTheme"])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
            self.characterWidget = NoahIntroScreen(
                character, transition_callback=self.showMapScreen
            )
        else:
            raise Exception(
                f"Introscreen for {character.name} has not yet been implemented"
            )

        self.stack.addWidget(self.characterWidget)
        self.stack.setCurrentWidget(self.characterWidget)

    def displayMonologue(self, character, event_id):
        self.stopAllSounds()
        if character.name == "John":
            # load monologue music
            pygame.mixer.music.load(AUDIO["JohnTheme"])
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        # Create a monologue widget for the character and set the transition callback to show the map screen after the monologue
        self.monologue = MonologueWidget(character, event_id, self.showMapScreen)
        self.stack.addWidget(self.monologue)
        self.stack.setCurrentWidget(self.monologue)

    def showMapScreen(self):
        self.stack.removeWidget(self.characterWidget)
        self.stopAllSounds()
        pygame.mixer.music.load(AUDIO["MapScreenMusic"])
        pygame.mixer.music.set_volume(0.9)
        pygame.mixer.music.play(loops=-1)

        self.mapScreen.map.setRoom(None)
        unbeaten = self.mapScreen.map.available_rooms()
        if len(unbeaten) > 0:
            self.mapScreen.map.setRoom(unbeaten[0])
        self.stack.setCurrentWidget(self.mapScreen)

    def playDialogue(self, room: dict):
        if not self.player:
            raise Exception("playDialogue expects a player")

        screen = DialogueScreen(self.player, room["NPC"])

        def dialogue_ended():
            self.stack.removeWidget(screen)
            self.EnterFight(room)

        screen.onComplete(dialogue_ended)
        self.stack.addWidget(screen)
        self.stack.setCurrentWidget(screen)
        return

    def EnterFight(self, room: dict):
        """
        Enter fight screen by pointing stack at fight screen.
        This will need to be changed to set the proper opponent per setting. Index 2 is the fight screen.
        """
        self.stopAllSounds()
        if not self.player:
            raise Exception("Cannot enter fight when no player is selected")

        if self.fight:
            self.stack.removeWidget(self.fight.widget)

        self.fight = FightSequence(self.player, room["NPC"], room["battlefield"])
        self.fight.onWin(lambda: self.showVictoryScreen(room["NPC"].name))
        self.fight.onLose(self.showDefeatScreen)
        self.fight.onWinGame(self.showWinGameCrawl)

        self.stack.addWidget(self.fight.widget)
        self.fight.widget.animation_Object.start()
        self.stack.setCurrentWidget(self.fight.widget)

    def saveCharacter(self, character: Character):
        CharacterFactory.SaveCharacter(character)

    def loadCharacter(self, name: str) -> Character:
        return CharacterFactory.LoadCharacter(name)

    def showVictoryScreen(self, boss_name):
        event_id = EventIdentifier.get_event_id("boss_defeat", boss_name)
        if self.fight is None:
            raise Exception("Victory Screen expects a fight")
        victory = VictoryScreen(self.fight)

        def loot_collected():
            self.stack.removeWidget(victory)
            if should_display_monologue(self.player, self.fight.enemy):
                self.displayMonologue(self.player, event_id)
            else:
                self.showMapScreen()

        victory.onClose(loot_collected)
        self.stack.addWidget(victory)
        self.fight.widget.animation_Object.stop()
        self.stack.setCurrentWidget(victory)

    def showWinGameCrawl(self):
        crawl = Crawl()
        crawl.text_lines = [
            "With their final year completed and the SENG program defunct, the students",
            "leave the institution, unprepared and unsatisfied with their educational experience.",
            "",
            "Instead of knowledge, they leave with debt. In place of job prospects, an endless",
            "job search reliant of the goodwill of potential employers. They leave knowing the",
            "diploma they possess isn’t worth the paper it is printed on.",
        ]
        crawl.onFinish(self.showCreditScreen)
        self.stack.addWidget(crawl)
        self.stack.setCurrentWidget(crawl)
        self.player.reset()
        self.stopAllSounds()

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
        if self.fight:
            self.fight.widget.animation_Object.stop()

    def showCreditScreen(self):
        credits = Credits()
        self.stack.addWidget(credits)
        self.stack.setCurrentWidget(credits)
        credits.onFinishCredits(self.showStartMenu)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_C:
            self.stopAllSounds()
            self.showCreditScreen()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.showMaximized()
    sys.exit(app.exec())
