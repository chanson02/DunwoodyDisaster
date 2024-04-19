import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QApplication
from dunwoody_disaster.views.fightScreen import FightScreen
from dunwoody_disaster.views.StartMenu import StartMenu
from dunwoody_disaster.views.MapScreen import MapScreen


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
    app = QApplication(sys.argv)  # Create an instance of QApplication
    startMenu = StartMenu()  # Create an instance of StartMenu
    startMenu.show()  # Show the StartMenu window in windowed mode 
    sys.exit(app.exec())  # Start the application's event loop and exit when it finishes