from typing import Callable
from dunwoody_disaster.CharacterFactory import CharacterFactory
from dunwoody_disaster.views.fightScreen import FightScreen
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QMessageBox,
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QPainter

# from dunwoody_disaster.views.MapScreen import MapScreen
from dunwoody_disaster import ASSETS, unimplemented


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self._callback = unimplemented
        self.background_pixmap = QPixmap(ASSETS["TitleScreen"])
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Game Start Menu")

        screen_size = (
            QApplication.primaryScreen().size()
        )  # Get the size of the primary screen
        self.resize(
            int(screen_size.width() * 0.8), int(screen_size.height() * 0.8)
        )  # Set the window size to 80% of the screen size

        main_layout = QVBoxLayout(self)

        title = QLabel("Dunwoody Disaster")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_layout.addWidget(title)

        button_layout = QHBoxLayout()

        self.startButton = QPushButton("Start Game")
        self.startButton.clicked.connect(self._callback)

        button_layout.addWidget(self.startButton)

        self.exitButton = QPushButton("Exit")
        self.exitButton.clicked.connect(self.exitGame)
        button_layout.addWidget(
            self.exitButton
        )  # Add the exit button to the button layout

        main_layout.addStretch(
            1
        )  # Add a stretchable space to push the buttons to the bottom
        main_layout.addLayout(button_layout)  # Add the button layout to the main layout

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
        self._callback = callback

    def paintEvent(self, event):
        _ = event  # silence unused warning
        painter = QPainter(self)  # Create a QPainter object for drawing
        pixmap = self.background_pixmap.scaledToWidth(400)
        painter.drawPixmap(self.rect(), pixmap)  # Draw the scaled pixmap on the window

    def exitGame(self):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.close()
