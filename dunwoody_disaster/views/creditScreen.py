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
        self.text_lines = [
            ("Cooper", "Lead Programmer | Resident Git Expert"),
            ("Noah", "Stock"),
            ("John", "Arts and Audio Director"),
            ("Mitch", "Stock"),
            ("Jenni", "Stock"),
        ]
        self.images = {
            "Cooper": DD.ASSETS["CooperRefined+"],
            "Noah": DD.ASSETS["NoahRefined+"],
            "John": DD.ASSETS["JohnRefined+"],
            "Mitch": DD.ASSETS["MitchRefined+"],
            "Jenni": DD.ASSETS["Jenni"],
        }
        self.current_line = 0
        self.opacity = 0.0
        self.fade_in = True
        self.pause = False
        self.initUI()
        self.initSound()

        # Timer to update opacity for fade-in and fade-out
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateOpacity)
        self.timer.start(50)  # Shorter interval for smoother transition

        self.pauseTimer = QTimer(self)
        self.pauseTimer.setSingleShot(True)
        self.pauseTimer.timeout.connect(self.startFadingOut)

    def initUI(self):
        self.setWindowTitle("End Credits")  # Set the window title
        self.setGeometry(100, 100, 1920, 1080)  # Set the window geometry
        self.timer = QTimer(self)  # Create a timer
        self.timer.timeout.connect(
            self.updateOpacity
        )  # Connect the timer to updateOpacity function
        self.timer.start(100)  # Start the timer with an interval of 100 milliseconds
        self.show()  # Show the widget

    def startFadingOut(self):
        self.fade_in = False
        self.pause = False
        self.timer.start(50)  # Resume timer for fading out

    def updateOpacity(self):
        if self.fade_in and not self.pause:
            if self.opacity < 1.0:
                self.opacity += 0.05
            else:
                # After fully fading in, pause for 5 seconds
                self.timer.stop()
                self.pause = True
                self.pauseTimer.start(5000)  # 5000 ms pause
        elif not self.fade_in:
            if self.opacity > 0:
                self.opacity -= 0.05
            else:
                # Once fully faded out, move to the next line or end
                self.fade_in = True
                self.current_line += 1
                if self.current_line >= len(self.text_lines):
                    self.endCreditScreen()
                    return
                self.timer.start(50)  # Start fading in the next line
        self.update()

    def paintEvent(self, event):
        # Check if there are no more lines to display and return early if true
        if self.current_line >= len(self.text_lines):
            return

        # Unpack the current line to get the name and description
        name, description = self.text_lines[self.current_line]

        # Initialize QPainter for drawing operations
        painter = QPainter(self)
        # Set rendering hints for smoother drawing
        painter.setRenderHint(QPainter.Antialiasing)
        # Set the brush color to black for filling the background
        painter.setBrush(Qt.black)
        # Fill the entire widget with a black background
        painter.fillRect(self.rect(), Qt.black)
        # Set the opacity for the fade effect
        painter.setOpacity(self.opacity)

        # Load and scale the image associated with the current name to half the screen width
        image = QPixmap(self.images[name])
        image = image.scaled(
            self.width() // 2,
            self.height(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation,
        )
        # Draw the image aligned to the left side, vertically centered
        painter.drawPixmap(0, (self.height() - image.height()) / 2, image)

        # Set the font for drawing text
        font = QFont("Arial", 24)
        painter.setFont(font)
        # Set the pen color to white for text drawing
        painter.setPen(QColor(255, 255, 255))

        # Calculate the start and width of the area where text will be centered (right half of the screen)
        text_area_start = self.width() // 2
        text_area_width = self.width() // 2

        # Calculate the width of the text to center it within the right half
        name_width = painter.fontMetrics().horizontalAdvance(name)
        description_width = painter.fontMetrics().horizontalAdvance(description)
        # Calculate the x-coordinate for the name and description to center them
        name_x = text_area_start + (text_area_width - name_width) // 2
        description_x = text_area_start + (text_area_width - description_width) // 2
        # Determine the vertical positions for the name and description
        name_y = (self.height() // 2) - 30
        desc_y = (self.height() // 2) + 30

        # Draw the name and description centered on the right half of the screen
        painter.drawText(name_x, name_y, name)
        painter.drawText(description_x, desc_y, description)

    def initSound(self):
        pygame.mixer.init()
        self.EndTheme = pygame.mixer.Sound(AUDIO["EndTheme"])
        self.EndTheme.set_volume(0.9)
        self.EndTheme.play()  # Play the end theme sound once

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
