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
        self.set_text("Filled with hope and the dream of becoming software engineers, four students will undertake a new journey each excited at the prospect of starting a new chapter in their lives.\n"
                      "\nDuring their time at Dunwoody, they will experience a new form of education. An education devoid of thought, planning, or reason whose sole purpose is to burden unsuspecting students with financial strife while providing few avenues for employment. \nNow, these four students must band together, united under one front, to dismantle the system that has crippled them financially, but provided so little in return. This is their story…")
        self.text_speed = 4  # Adjusted for faster scrolling on larger resolution

        self.text_y = self.height()  # Initialize text_y to the height of the window

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_text)
        self.timer.start(20)

    def set_text(self, textInput: str):
        self.text = textInput

    def move_text(self):
        text_height = QFontMetrics(QFont("Arial", 24)).boundingRect(QRect(0, 0, self.width(), self.height()), Qt.TextWordWrap, self.text).height()

        self.text_y -= self.text_speed
        if self.text_y < -text_height:
            self.text_y = self.height()

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

        painter.drawText(text_x, self.text_y, bounding_rect.width(), bounding_rect.height(), Qt.AlignCenter, self.text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovingTextWidget()
    window.show()
    sys.exit(app.exec())
