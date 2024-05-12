import pygame
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QColor, QFont, QPainter, QPixmap, QKeyEvent
from PySide6.QtWidgets import QWidget
import dunwoody_disaster as DD
from dunwoody_disaster import AUDIO
from typing import Callable


class Credits(QWidget):
    def __init__(self):
        super().__init__()
        self._finishCallback = (
            DD.unimplemented
        )  # Set up a finish callback, currently unimplemented in DD
        self.text_lines = [  # List of names to display in the credits
            "Cooper",
            "Noah",
            "John",
            "Mitch",
        ]
        self.images = {
            "Cooper": DD.ASSETS["CooperRefined+"],
            "Noah": DD.ASSETS["NoahRefined+"],
            "John": DD.ASSETS["JohnRefined+"],
            "Mitch": DD.ASSETS["MitchRefined+"],
        }
        self.current_line = 0  # Start displaying from the first line
        self.opacity = 0.0  # Initial opacity for fade effect set to 0
        self.fade_in = True  # Flag to check if fading in or out
        self.initUI()  # Initialize the UI setup
        self.initSound()  # Initialize the sound setup

    def initUI(self):
        self.setWindowTitle("Story Crawl")  # Set the window title
        self.setGeometry(100, 100, 1920, 1080)  # Set the window geometry
        self.timer = QTimer(self)  # Create a timer
        self.timer.timeout.connect(
            self.updateOpacity
        )  # Connect the timer to updateOpacity function
        self.timer.start(100)  # Start the timer with an interval of 100 milliseconds
        self.show()  # Show the widget

    def updateOpacity(self):
        if self.fade_in:  # Check if currently in fade-in mode
            if self.opacity < 1.0:  # If opacity is less than 1
                self.opacity += 0.05  # Increase opacity
            else:
                self.fade_in = False  # Switch to fade-out mode
        else:  # If not in fade-in mode
            if self.opacity > 0:  # If opacity is greater than 0
                self.opacity -= 0.05  # Decrease opacity
            else:
                self.fade_in = True  # Switch to fade-in mode
                self.current_line += 1  # Move to next line
                if self.current_line >= len(
                    self.text_lines
                ):  # If all lines are processed
                    self.endCreditScreen()  # End the credit screen
                    return
        self.update()  # Update the widget to repaint

    def paintEvent(self, event):
        if self.current_line >= len(
            self.text_lines
        ):  # Exit early if there are no lines left to display
            return
        line = self.text_lines[self.current_line]  # Get the current line
        painter = QPainter(self)  # Start a painter
        painter.setRenderHint(QPainter.Antialiasing)  # Enable smoother drawing
        painter.setBrush(Qt.black)  # Set the brush to black for background
        painter.fillRect(self.rect(), Qt.black)  # Fill the background with black
        painter.setOpacity(self.opacity)  # Set the opacity for fading effect

        image = QPixmap(self.images[line])  # Load the pixmap for the current line
        # Scale image to fill half the width of the window, maintaining aspect ratio
        image = image.scaled(
            self.width() // 2,
            self.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        painter.drawPixmap(
            0, (self.height() - image.height()) / 2, image
        )  # Draw the pixmap aligned to the left

        # Update font settings
        font = QFont("Arial", 24)  # Use a 24-point Arial font
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))  # Set the pen to white for text

        # Calculate the x-coordinate for the text to appear to the right of the image
        x = (
            self.width() // 2
            + (self.width() // 2 - painter.fontMetrics().horizontalAdvance(line)) / 2
        )
        y = (
            self.height() - painter.fontMetrics().height()
        ) / 2  # Center the text vertically
        painter.drawText(x, y, line)  # Draw the text

    def initSound(self):
        pygame.mixer.init()
        self.EndTheme = pygame.mixer.Sound(AUDIO["EndTheme"])
        self.EndTheme.set_volume(0.9)
        self.EndTheme.play()  # Play the end theme sound indefinitely

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            self.endCreditScreen()

    def endCreditScreen(self):
        self.EndTheme.stop()
        self.timer.stop()
        if self._finishCallback:
            self._finishCallback()
        self.deleteLater()

    def onFinishCredits(self, callback: Callable):
        self._finishCallback = callback
