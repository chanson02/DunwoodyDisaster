import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QStackedWidget,
    QLabel,
)

from StartMenuTest import (
    StartMenu,
)  # Assuming StartMenuTest.py contains StartMenu class
from MapScreen import MapScreen  # Assuming MapScreen.py contains MapScreen class


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initialize the QStackedWidget and pages
        self.stack = QStackedWidget()
        self.startMenu = StartMenu()
        self.mapScreen = MapScreen()

        self.stack.addWidget(self.startMenu)
        self.stack.addWidget(self.mapScreen)

        # Set the stacked widget as the central widget of the main window
        self.setCentralWidget(self.stack)
        self.setWindowTitle("Game")

        # Connect signals to slots for page switching
        self.startMenu.startButton.clicked.connect(self.showMapScreen)

    def showMapScreen(self):
        self.stack.setCurrentIndex(1)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
