from typing import Callable

from PySide6.QtGui import QPixmap
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

        backgroundPic_Lbl = QLabel()
        background_pixmap = QPixmap(ASSETS["TitleScreen"]).scaledToHeight(700)
        backgroundPic_Lbl.setPixmap(background_pixmap)

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
            self.close()
