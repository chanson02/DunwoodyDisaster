import sys
from dunwoody_disaster.views.AnimationWidget import AnimationWidget
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
)
from dunwoody_disaster.animations.basic_attack import AttackAnimation
from dunwoody_disaster.animations.idle import IdleAnimation
import dunwoody_disaster as DD
from PySide6.QtCore import QTimer
from PySide6.QtCore import Signal


class MainWindow(QMainWindow):
    sig = Signal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        btn = QPushButton("Switch")
        btn.clicked.connect(self.switch)

        self.idle = IdleAnimation(
            DD.ASSETS["CourtYard"], DD.ASSETS["cooper"], DD.ASSETS["no_texture"]
        )
        self.animation = AnimationWidget()
        self.animation.setAnimation(self.idle)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.animation)
        wid = QWidget()
        wid.setLayout(layout)
        self.setCentralWidget(wid)

    def switch(self):
        attack = AttackAnimation(
            DD.ASSETS["CourtYard"],
            DD.ASSETS["cooper"],
            DD.ASSETS["no_texture"],
            DD.ASSETS["no_texture"],
            self.sig,
        )
        self.sig.connect(self.perform_switch_back)
        self.animation.setAnimation(attack)

    def perform_switch_back(self):
        self.animation.setAnimation(self.idle)

    def closeEvent(self, event):
        _ = event  # silence unused warning
        self.animation.stop()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
