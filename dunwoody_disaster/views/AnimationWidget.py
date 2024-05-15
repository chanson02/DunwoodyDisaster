from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import threading
from PySide6.QtGui import QPixmap
from PySide6.QtCore import QTimer
from queue import Queue
from dunwoody_disaster.animations.PygameAnimation import PygameAnimation


# Defines AnimationWidget as a subclass of QWidget, allowing it to inherit all methods and properties of a Qt widget.
class AnimationWidget(QWidget):
    def __init__(self, animation: PygameAnimation):
        super().__init__()
        self.animation = animation
        self.init_ui()

        self.queue = Queue()
        self.engine_thread = threading.Thread(target=self.update_frame)
        self.timer = QTimer()
        self.timer.timeout.connect(self.draw_frames)

    def setAnimation(self, animation: PygameAnimation):
        self.animation = animation
        self.start()

    def start(self):
        self.stop()
        self.engine_thread = threading.Thread(target=self.update_frame)
        if self.animation.running:
            raise Exception(f"{self.animation} already running.")
        self.setMinimumHeight(self.animation.size[1])
        self.setMinimumWidth(self.animation.size[0])
        self.animation.start()
        self.timer.start(100)
        if not self.engine_thread.is_alive():
            self.engine_thread.start()

    def stop(self):
        self.animation.running = False
        self.timer.stop()
        if self.engine_thread.is_alive():
            self.engine_thread.join()

    def init_ui(self):
        layout = QVBoxLayout()
        self.frame = QLabel()
        layout.addWidget(self.frame)
        self.setLayout(layout)

    def update_frame(self):
        while self.animation.running:
            self.animation.run()
            self.queue.put(self.animation.to_qimage())

    def draw_frames(self):
        while not self.queue.empty():
            self.frame.setPixmap(QPixmap.fromImage(self.queue.get()))
