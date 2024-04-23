import sys, json
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel

# from dunwoody_disaster.views.dialogueScreen import DialogueScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory

# from dunwoody_disaster.views.MapScreen import MapScreen
# from dunwoody_disaster.views.FightPreview import FightPreview

# from dunwoody_disaster.views.defeatScreen import DefeatScreen
from dunwoody_disaster import ASSETS
# from dunwoody_disaster.views.CharacterSelector import CharacterSelector
import pygame
import threading
import queue
from PySide6.QtCore import QThread, QTimer
from PySide6.QtGui import QPixmap, QImage
from dunwoody_disaster.animations.TestAnimation import TestAnimation
from dunwoody_disaster.views.AnimationWidget import AnimationWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")

        test_animation = TestAnimation()
        self.animation = AnimationWidget(test_animation)

        self.setCentralWidget(self.animation)
        self.animation.start()

    def closeEvent(self, event):
        self.animation.stop()

if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
