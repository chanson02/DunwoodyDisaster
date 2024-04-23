from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import threading
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from queue import Queue
from dunwoody_disaster.animations import PygameAnimation


class AnimationWidget(QWidget):
    def __init__(self, animation: PygameAnimation):
        self.animation = animation
        self.init_ui()

        self.queue = Queue()
        self.engine_thread = threading.Thread(target=self.draw_frames)
        self.engine_thread.start()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def init_ui(self):
        layout = QVBoxLayout()
        self.frame = QLabel()
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def update_frame(self):
        self.animation.run()
        img_bytes = self.animation.to_bytes()
        self.queue.put(img_bytes)

    def draw_frames(self):
        while not self.queue.empty():
            img_bytes = self.queue.get()
            img = QImage(img_bytes, 800, 600, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.frame.setPixmap(pixmap)
