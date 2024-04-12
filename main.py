"""
The entry point for the game
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from dunwoody_disaster.views.fightScreen import FightScreen

from StartMenu import StartMenu
from MapScreen import MapScreen  # Assuming MapScreen.py contains MapScreen class

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dunwoody-Disaster")
        # self.setGeometry(100, 100, 800, 600)

        self.startMenu = StartMenu()
        self.startMenu.startButton.clicked.connect(self.showMapScreen)
        self.mapScreen = MapScreen()
        self.fightScreen = FightScreen()

        self.stack = QStackedWidget()
        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)
        self.stack.addWidget(self.fightScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)

    def showMapScreen(self):
        self.stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
