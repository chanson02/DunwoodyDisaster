import pygame

from typing import Callable

from PySide6.QtGui import QMovie, QPainter
from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QWidget,
    QApplication,
    QSpacerItem,
    QSizePolicy,
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
        maybeSize = self._movieSize.scaled(
            cr.size(), Qt.AspectRatioMode.KeepAspectRatio
        )

        if maybeSize != movie.scaledSize():
            movie.setScaledSize(maybeSize)
            style.drawItemPixmap(
                qp,
                cr,
                alignment,
                movie.currentPixmap().scaled(
                    cr.size(), Qt.AspectRatioMode.KeepAspectRatio
                ),
            )

        else:
            style.drawItemPixmap(qp, cr, alignment, movie.currentPixmap())


class StartMenu(QWidget):
    def __init__(self):
        super().__init__()
        self._callback = DD.unimplemented

        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        self.movie = QMovie(DD.ASSETS["FinalTitle"])

        row = 0

        # layout.addItem(
        #     QSpacerItem(0, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 0)

        bkg = MovieLabel()
        bkg.setMovie(self.movie)
        bkg.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(bkg, row, 0)

        # layout.addItem(
        #     QSpacerItem(0, 20, QSizePolicy.Fixed, QSizePolicy.MinimumExpanding), 2, 0)

        btns_Lyt = QGridLayout()
        layout.addLayout(btns_Lyt, row, 0)
        btn_style = "background-color: transparent; min-width: 400px; font-size: 36px; font-weight: 600px;"

        btns_Lyt.addItem(
            QSpacerItem(
                0, 50, QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
            ),
            0,
            0,
        )

        start = QPushButton("Start Game")
        start.setStyleSheet(btn_style)
        start.clicked.connect(self.startClicked)
        btns_Lyt.addWidget(start, 1, 1)

        btns_Lyt.addItem(
            QSpacerItem(50, 170, QSizePolicy.MinimumExpanding, QSizePolicy.Fixed), 2, 2
        )

        # close = QPushButton("Exit")
        # close.setStyleSheet(btn_style)
        # close.clicked.connect(self.exitGame)
        # btns_Lyt.addWidget(close)

        # btns_Lyt.addItem(
        #     QSpacerItem(50, 0, QSizePolicy.Fixed, QSizePolicy.Fixed))

        # layout.addItem(
        #     QSpacerItem(0, 50, QSizePolicy.Fixed, QSizePolicy.Fixed), 4, 0)

    def startClicked(self):
        self.movie.stop()
        self._callback()

    def onStart(self, callback: Callable):
        """
        A callback function that executes when the user presses start
        """
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
