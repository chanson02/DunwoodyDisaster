import sys
from dunwoody_disaster.views.AnimationWidget import AnimationWidget
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QVBoxLayout
from dunwoody_disaster.animations.basic_attack import AttackAnimation
from dunwoody_disaster.animations.idle import IdleAnimation
import dunwoody_disaster as DD


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")
        btn = QPushButton("Switch")
        btn.clicked.connect(self.switch)

        idle = IdleAnimation(DD.ASSETS["CourtYard"], DD.ASSETS["cooper"], DD.ASSETS["no_texture"])
        #self.animation = AnimationWidget(idle)
        self.animation = AnimationWidget()
        self.animation.setAnimation(idle)

        layout = QVBoxLayout()
        layout.addWidget(btn)
        layout.addWidget(self.animation)
        wid = QWidget()
        wid.setLayout(layout)
        self.setCentralWidget(wid)
        # self.animation.start()

    def switch(self):
        self.animation.setAnimation(AttackAnimation())


    def closeEvent(self, event):
        _ = event  # silence unused warning
        self.animation.stop()


if __name__ == "__main__":
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
