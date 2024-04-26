from PySide6.QtCore import Qt
from PySide6.QtGui import QKeyEvent
from PySide6.QtWidgets import (
    QWidget,
    QStackedLayout,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QGroupBox,
)
import dunwoody_disaster as DD

class Crawl(QWidget):
    def __init__(self):
        """A screen to show an opening (or closing) crawl.
            The text will move from the bottom of the screen to the top of the screen."""
        super().__init__()
        self.movingText = []

    def SetText(self, textInput : list[str]):
        self.movingText = textInput

    def keyPressEvent(self, event: QKeyEvent):
        if(event.key() == Qt.Key.Key_Return):
            print("End")

    
