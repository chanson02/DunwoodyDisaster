import sys
from PySide6.QtCore import Qt, QTimer
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

        self.text_y = (self.height() - QFontMetrics(QFont("Arial", 24)).boundingRect(self.text).height()) / 2
        self.text_x = (self.width() - QFontMetrics(QFont("Arial", 24)).boundingRect(self.text).width()) / 2

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_text)
        self.timer.start(20)

    def move_text(self):
        self.text_y -= self.text_speed
        if self.text_y < - QFontMetrics(QFont("Arial", 24)).boundingRect(self.text).height():
            self.text_y = self.height()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        painter.setPen(QColor(Qt.yellow))
        font = QFont("Arial", 24)
        painter.setFont(font)

        painter.drawText(self.text_x, self.text_y, self.width(), self.height(), Qt.AlignLeft | Qt.TextWordWrap, self.text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovingTextWidget()
    window.show()
    sys.exit(app.exec())
