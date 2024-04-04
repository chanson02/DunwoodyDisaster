"""
The entry point for the game
"""

import sys
from os import path
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget, QLabel
from PySide6.QtGui import QPixmap, QKeyEvent
from dunwoody_disaster import ASSETS


class MapScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.mainLayout = QGridLayout(spacing=0)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.mapPic = QLabel("")
        self.mapPic.setPixmap(QPixmap(ASSETS["CourtYard"]))
        self.mainLayout.addWidget(self.mapPic, 0, 0)

        self.imagePaths = [
            ASSETS[img]
            for img in ["CourtYard", "LectureHall", "Physics", "Science Lab"]
        ]

        self.currImgIndex = 0

    def keyPressEvent(self, event: QKeyEvent):
        print("entering")
        if event.key() == Qt.Key_Left:
            self.currImgIndex = (self.currImgIndex - 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("left")

        elif event.key() == Qt.Key_Right:
            self.currImgIndex = (self.currImgIndex + 1) % len(self.imagePaths)
            self.mapPic.setPixmap(QPixmap(self.imagePaths[self.currImgIndex]))
            print("right")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Call the parent class constructor
        self.setWindowTitle("Map")  # Set the window title

        # Set the central widget of the main window to be an instance of MapScreen
        self.setCentralWidget(MapScreen())
        self.centralWidget().setFocus()  # Set focus to the MapScreen widget for key events


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create a QApplication instance
    window = MainWindow()  # Create the main window
    window.showMaximized()  # Show the main window maximized
    sys.exit(app.exec())  # Start the application event loop and exit when done
