import pygame

from typing import Callable

from PySide6.QtGui import QMovie
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QApplication,
)

from dunwoody_disaster import ASSETS, unimplemented


class MovieLabel(QLabel):
    def __init__(self, movie_path, parent=None):
        super().__init__(parent)
        self.movie = QMovie(movie_path)
        self.setMovie(self.movie)
        self.movie.start()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.movie.setScaledSize(self.size())  # Scale movie to the size of the label


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")
        self.setWindowTitle("Dunwoody Disaster")

        main_layout = QGridLayout(self)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Setup the MovieLabel to display the GIF dynamically
        backgroundPic_Lbl = MovieLabel(ASSETS["FinalTitle"], self)
        main_layout.addWidget(backgroundPic_Lbl, 1, 1)

        button_layout = QGridLayout()
        self.startButton = QPushButton("Start Game")
        self.startButton.setStyleSheet(
            "background-color: gray; min-width: 250px; font-size: 14px; font-weight: 600px;"
        )
        self.startButton.clicked.connect(unimplemented)
        button_layout.addWidget(self.startButton, 0, 1)

        self.exitButton = QPushButton("Exit")
        self.exitButton.setStyleSheet(
            "background-color: gray; min-width: 250px; font-size: 14px; font-weight: 600px;"
        )
        self.exitButton.clicked.connect(self.exitGame)
        button_layout.addWidget(self.exitButton, 0, 2)

        main_layout.addLayout(button_layout, 2, 1)

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
        self.startButton.clicked.disconnect()
        self.startButton.clicked.connect(callback)

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
            QApplication.quit()
