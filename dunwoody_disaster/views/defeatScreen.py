from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QScrollArea,
    QGroupBox,
)
from PySide6.QtWidgets import QApplication, QMainWindow
import sys

styles = {
    "title-text": "color: white; font-size: 24px;",
    "center": "margin-left: auto; margin-right: auto;",
    "return-button": "border-radius: 15px; height: 42px; background-color: white; color: black; font-size: 24px; width: 200px;",
}


class DefeatScreen(QWidget):
    def __init__(self, image: str = None):
        """
        Creates a screen to display that you have lost with a button to return to the map
        :param image: the path to the image to display
        """
        super().__init__()

        self.show = True

        self.image = image

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        container = QVBoxLayout()
        container.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # UI Elements
        # Game over label
        defeat_label = QLabel("You have been defeated")
        defeat_label.setStyleSheet(styles["title-text"] + styles["center"])

        # Return Button
        return_button = QPushButton("Return to Map")
        return_button.setStyleSheet(styles["return-button"] + styles["center"])
        return_button.clicked.connect(self.return_to_map)

        # Add defeat Image
        if self.image is not None:
            defeat_image = QPixmap(self.image)
            Imagelabel = QLabel(self)
            Imagelabel.setPixmap(defeat_image)
            container.addWidget(Imagelabel)

        container.addWidget(defeat_label)
        container.addWidget(return_button)
        layout.addLayout(container)
        self.setLayout(layout)

    # Functions
    def return_to_map(self):
        """
        Returns the player to the map screen

        """
        self.show = False

    def SetImage(self, image: str):
        """
        Sets the image to display on the screen
        :param image: the path to the image to display
        """
        self.image = QPixmap(image)
        self.label.setPixmap(self.image)


# For testing purposes
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Pokemon-like Game")
#         self.setGeometry(100, 100, 800, 600)
#         self.setStyleSheet("background-color: #2f2f2f;")

#         if 1 == 2:  # this is here to clear lint warnings
#             self.setCentralWidget(DefeatScreen())
#         else:
#             self.setCentralWidget(DefeatScreen("dunwoody_disaster/assets/ready.jpg"))


# if __name__ == "__main__":
#     app = QApplication()
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec())
