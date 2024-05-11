from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
import threading
from PySide6.QtGui import QPixmap, QImage
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

    # data must be 32-bit aligned, and each scanline of data in the image must also be 32-bit aligned
    def update_frame(self):
        while self.animation.running:
            self.animation.run()
            img_bytes = self.animation.to_bytes()
            self.queue.put(img_bytes)

    """
    Try this constructor for QImage
        def __init__(self, data: Union[bytes, bytearray, memoryview], width: int, height: int, bytesPerLine: int, format: PySide7.QtGui.QImage.Format, cleanupFunction: Optional[Callable] = ..., cleanupInfo: Optional[int] = ...) -> None: ...
    """
    def draw_frames(self):
        width = self.animation.size[0]
        height = self.animation.size[1]
        while not self.queue.empty():
            img_bytes = self.queue.get()
            img = QImage(img_bytes, width, height, 1998, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            self.frame.setPixmap(pixmap)
