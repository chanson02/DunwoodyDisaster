from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
)
from typing import Callable
import dunwoody_disaster as DD

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
        
        self._callback = DD.unimplemented
        
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

        # Add elements to layout
        container.addWidget(defeat_label)
        container.addWidget(return_button)
        layout.addLayout(container)
        self.setLayout(layout)

    # Functions
    def return_to_map(self):
        """
        Returns the player to the map screen
        """
        self.deleteLater()
        self._callback()

    def SetImage(self, image: str):
        """
        Sets the image to display on the screen
        :param image: the path to the image to display
        """
        self.image = QPixmap(image)
        self.label.setPixmap(self.image)

    def onClose(self, callback: Callable):
        """
        Sets the callback function to be called when the return button is clicked
        :param callback: the function to be called
        """
        self._callback = callback