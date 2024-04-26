import sys
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

class MovingTextWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Moving Text Example")
        self.setGeometry(100, 100, 1280, 720)  # Adjusted for 1080p monitor

        self.text = "Scrolling Text. Lorem ipsum dolor sit amet, consectetur adipiscing elit. " \
                    "Integer nec odio. Praesent libero. Sed cursus ante dapibus diam. Sed nisi."
        self.text_speed = 4  # Adjusted for faster scrolling on larger resolution

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_text)
        self.timer.start(20)

    def move_text(self):
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        painter.setPen(QColor(Qt.yellow))
        font = QFont("Arial", 24)
        painter.setFont(font)

        text_rect = QRect(0, 0, self.width(), self.height())
        bounding_rect = QFontMetrics(font).boundingRect(text_rect, Qt.TextWordWrap, self.text)

        text_x = (self.width() - bounding_rect.width()) / 2
        text_y = (self.height() - bounding_rect.height()) / 2

        painter.drawText(text_x, text_y, bounding_rect.width(), bounding_rect.height(), Qt.AlignCenter, self.text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovingTextWidget()
    window.show()
    sys.exit(app.exec())
