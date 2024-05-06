import pygame

from typing import Callable

from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap, QMovie
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QSizePolicy,
    QSpacerItem,
)

from dunwoody_disaster import ASSETS, unimplemented


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setupMusicPlayer()

    def setupMusicPlayer(self):
        # Initialize Pygame mixer
        pygame.mixer.init()
        # Load and play background music
        pygame.mixer.music.load(
            "C:/Users/vuejo/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/audio/TitleScreenMusic.wav"
        )
        pygame.mixer.music.set_volume(0.75)  # Set volume from 0.0 to 1.0
        pygame.mixer.music.play(-1)  # Play indefinitel

    def initUI(self):
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Dunwoody Disaster")

        main_layout = QGridLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        main_layout.addItem(
            QSpacerItem(
                5, 5, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            0,
            0,
        )

        # Setup the QLabel to display the GIF
        backgroundPic_Lbl = QLabel(self)
        # Initialize QMovie with the path to the GIF
        movie = QMovie(
            "C:/Users/vuejo/OneDrive - Dunwoody College of Technology/Documents/Data Structures/Class/DunwoodyDisaster/dunwoody_disaster/animations/Animation_Assets/TitleScreenFinal.gif"
        )
        backgroundPic_Lbl.setMovie(movie)
        movie.setScaledSize(QSize(1280, 720))  # Optional: Scale the movie size
        movie.start()  # Start playing the GIF

        main_layout.addWidget(backgroundPic_Lbl, 1, 1)

        button_layout = QGridLayout(self)
        button_layout.setContentsMargins(0, 0, 0, 0)

        self.startButton = QPushButton("Start Game")
        self.startButton.setStyleSheet("background-color: gray;")
        self.startButton.clicked.connect(unimplemented)

        button_layout.addItem(
            QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), 0, 0
        )

        button_layout.addWidget(self.startButton, 0, 1)

        button_layout.addItem(
            QSpacerItem(20, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), 0, 2
        )

        self.exitButton = QPushButton("Exit")
        self.exitButton.setStyleSheet("background-color: gray;")
        self.exitButton.clicked.connect(self.exitGame)
        button_layout.addWidget(
            self.exitButton, 0, 3
        )  # Add the exit button to the button layout

        button_layout.addItem(
            QSpacerItem(5, 0, QSizePolicy.Fixed, QSizePolicy.Fixed), 0, 4
        )

        main_layout.addLayout(
            button_layout, 2, 1
        )  # Add the button layout to the main layout

        main_layout.addItem(
            QSpacerItem(
                5, 5, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            3,
            2,
        )

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(callback)

    # def paintEvent(self, event):
    #     _ = event  # silence unused warning
    #     painter = QPainter(self)  # Create a QPainter object for drawing
    #     pixmap = self.background_pixmap.scaledToWidth(400)
    #     painter.drawPixmap(self.rect(), pixmap)  # Draw the scaled pixmap on the window

    def exitGame(self):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            pygame.mixer.music.stop()  # Stop the music
            self.close()
