import pygame

from typing import Callable

from PySide6.QtGui import QMovie, QPainter
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QApplication,
    QSizePolicy
)

import dunwoody_disaster as DD


# Got this from https://stackoverflow.com/questions/77602181/pyside6-how-do-i-resize-a-qlabel-playing-a-qmovie-and-maintain-the-movies-orig
class MovieLabel(QLabel):
    def __init__(self):
        super().__init__()
        self._movieSize = QSize()
        self._minSize = QSize()

    def minimumSizeHint(self):
        if self._minSize.isValid():
            return self._minSize
        return super().minimumSizeHint()

    def setMovie(self, movie: QMovie):
        if self.movie() == movie:
            return
        super().setMovie(movie)

        if not movie.isValid():
            self._movieSize = QSize()
            self._minSize = QSize()
            self.updateGeometry()
            return

        cf = movie.currentFrameNumber()
        state = movie.state()
        movie.jumpToFrame(0)
        rect = QRect()
        for i in range(movie.frameCount()):
            movie.jumpToNextFrame()
            rect |= movie.frameRect()

        width = rect.x() + rect.width()
        height = rect.y() + rect.height()

        self._movieSize = QSize(width, height)
        if width == height and False:
            if width < 4:
                self._minSize = QSize(width, width)
            else:
                self._minSize = QSize(4, 4)
        else:
            minimum = min(width, height)
            maximum = max(width, height)
            ratio = maximum / minimum
            base = min(4, minimum)
            self._minSize = QSize(base, round(base * ratio))
            if minimum == width:
                self._minSize.transpose()

        movie.jumpToFrame(cf)
        if state == movie.MovieState.Running:
            movie.setPaused(False)
        self.updateGeometry()

    def paintEvent(self, event):
        movie = self.movie()
        if not isinstance(movie, QMovie) or not movie.isValid():
            super().paintEvent(event)
            return

        qp = QPainter(self)
        self.drawFrame(qp)

        cr = self.contentsRect()
        margin = self.margin()
        cr.adjust(margin, margin, -margin, -margin)

        style = self.style()
        alignment = style.visualAlignment(self.layoutDirection(), self.alignment())
        maybeSize = self._movieSize.scaled(cr.size(), Qt.AspectRatioMode.KeepAspectRatio)

        if maybeSize != movie.scaledSize():
            movie.setScaledSize(maybeSize)
            style.drawItemPixmap(
                qp, cr, alignment, 
                movie.currentPixmap().scaled(cr.size(), Qt.AspectRatioMode.KeepAspectRatio)
            )

        else:
            style.drawItemPixmap(
                qp, cr, alignment, 
                movie.currentPixmap()
            )

class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self._callback = DD.unimplemented

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setStyleSheet('border: 1px solid green;')

        self.movie = QMovie(DD.ASSETS["FinalTitle"])
        self.movie.start()

        bkg = MovieLabel()
        bkg.setMovie(self.movie)
        bkg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(bkg)

        btns = QHBoxLayout()
        layout.addLayout(btns)
        btn_style = "background-color: gray; min-width: 250px; font-size: 14px; font-weight: 600px;"

        start = QPushButton("Start Game")
        start.setStyleSheet(btn_style)
        start.clicked.connect(self.startClicked)
        btns.addWidget(start)

        close = QPushButton("Exit")
        close.setStyleSheet(btn_style)
        close.clicked.connect(self.exitGame)
        btns.addWidget(close)

    def startClicked(self):
        self._callback()

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
        self.movie.stop()
        self._callback = callback

    def exitGame(self):
        reply = QMessageBox.question(
            self,
            "Exit",
            "Are you sure you want to exit?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            pygame.mixer.music.stop()  # Stop the music
            self.close()
            QApplication.quit()
