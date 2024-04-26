from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import threading
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import QTimer
from queue import Queue
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation


class AnimationWidget(QWidget):
    def __init__(self, animation: PygameAnimation):
        super().__init__()
        self.animation = animation
        self.init_ui()

        self.queue = Queue()
        self.engine_thread = threading.Thread(target=self.update_frame)
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_frames)

    def start(self):
        if self.animation.running:
            raise Exception(f"{self.animation} already running.")
        self.animation.start()
        self.engine_thread.start()
        self.timer.start(100)

    def stop(self):
        self.animation.running = False
        self.timer.stop()

    def init_ui(self):
        layout = QVBoxLayout()
        self.frame = QLabel()
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def update_frame(self):
        while self.animation.running:
            self.animation.run()
            img_bytes = self.animation.to_bytes()
            self.queue.put(img_bytes)

    def draw_frames(self):
        width = self.animation.size[0]
        height = self.animation.size[1]
        while not self.queue.empty():
            img_bytes = self.queue.get()
            img = QImage(img_bytes, width, height, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.frame.setPixmap(pixmap)
