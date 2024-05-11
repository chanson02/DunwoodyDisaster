import pygame

from typing import Callable

from PySide6.QtGui import QMovie
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QApplication,
)

import dunwoody_disaster as DD

class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self._callback = DD.unimplemented

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        bkg = QLabel("This is a test")
        bkg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        bkg.setStyleSheet('min-height: 500px; min-width: 500px;')
        self.movie = QMovie(DD.ASSETS["FinalTitle"])
        self.movie.start()
        bkg.setMovie(self.movie)
        layout.addWidget(bkg)

        btns = QHBoxLayout()
        layout.addLayout(btns)
        btn_style = "background-color: gray; min-width: 250px; font-size: 14px; font-weight: 600px;"

        start = QPushButton("Start Game")
        start.setStyleSheet(btn_style)
        start.clicked.connect(self.startClicked)
        btns.addWidget(start)

        close = QPushButton("Exit")
        close.setStyleSheet(btn_style)
        close.clicked.connect(self.exitGame)
        btns.addWidget(close)

    def startClicked(self):
        self._callback()

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
        self.movie.stop()
        self._callback = callback

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
