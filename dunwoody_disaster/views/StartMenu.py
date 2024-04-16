import sys
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
from dunwoody_disaster.views.MapScreen import MapScreen
from dunwoody_disaster import ASSETS


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()  # Call the constructor of the parent class (QWidget)
        self.background_pixmap = QPixmap(
            ASSETS["TitleScreen"]
        )  # Load the image as a QPixmap
        self.initUI()  # Initialize the user interface

    def initUI(self):
        self.setWindowTitle("Game Start Menu")  # Set the window title

        screen_size = (
            QApplication.primaryScreen().size()
        )  # Get the size of the primary screen
        self.resize(
            int(screen_size.width() * 0.8), int(screen_size.height() * 0.8)
        )  # Set the window size to 80% of the screen size

        main_layout = QVBoxLayout(self)

        title = QLabel("Dunwoody Disaster")
        title.setAlignment(Qt.AlignCenter)

        main_layout.addWidget(title)

        button_layout = QHBoxLayout()

        self.startButton = QPushButton("Start Game")
        self.startButton.clicked.connect(
            self.startGame
        )  # Connect to startGame function
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

    def paintEvent(self, event):
        painter = QPainter(self)  # Create a QPainter object for drawing
        pixmap = self.background_pixmap.scaledToWidth(400)
        painter.drawPixmap(self.rect(), pixmap)  # Draw the scaled pixmap on the window

    def startGame(self):
        print("clicked")
        self.game_page = MapScreen()  # Create an instance of the GamePage
        self.game_page.show()  # Show a message box when the start game button is clicked

    def exitGame(self):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )  # Ask for confirmation before exiting
        if reply == QMessageBox.Yes:
            self.close()  # Close the window if the user confirms


if __name__ == "__main__":
    app = QApplication(sys.argv)  # Create an instance of QApplication
    startMenu = StartMenu()  # Create an instance of StartMenu
    startMenu.show()  # Show the StartMenu window in windowed mode
    sys.exit(app.exec())  # Start the application's event loop and exit when it finishes
