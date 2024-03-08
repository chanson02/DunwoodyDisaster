"""
The entry point for the game
"""

import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from views.fight import FightScreen


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pokemon-like Game')
        self.setGeometry(100, 100, 800, 600)

        self.setCentralWidget(FightScreen())


if __name__ == '__main__':
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
