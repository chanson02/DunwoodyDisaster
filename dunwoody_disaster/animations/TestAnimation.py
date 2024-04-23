import pygame
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation
from typing import override


class TestAnimation(PygameAnimation):
    def __init__(self):
        super().__init__()

    @override
    def run(self) -> None:
        if self.running:
            self.surface.fill((255, 255, 255))
            pygame.draw.circle(self.surface, (255, 0, 0), (200, 150), 50)
            self.clock.tick(60)  # limit to 60 fps

"""
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("test")

        test_animation = TestAnimation()
        self.animation = AnimationWidget(test_animation)

        self.setCentralWidget(self.animation)
        self.animation.start()

    def closeEvent(self, event):
        self.animation.stop()

if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
"""
