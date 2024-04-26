import sys
from PySide6.QtCore import Qt, QRect, QTimer
from PySide6.QtGui import QColor, QFont, QFontMetrics, QPainter
from PySide6.QtWidgets import QApplication, QMainWindow

class MovingTextWidget(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Moving Text Example")
        self.setGeometry(100, 100, 1280, 720)  # Adjusted for 1080p monitor

        self.paragraphs = [
            "Paragraph 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
            "Paragraph 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
            "Paragraph 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
            "Paragraph 4: Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
            "Paragraph 5: Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
        ]

        self.text_speed = 4  # Adjusted for faster scrolling on larger resolution

        self.text_y = self.height()  # Initialize text_y to the height of the window
        self.current_paragraph = 0  # Index of the current paragraph being displayed

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_text)
        self.timer.start(20)

    def move_text(self):
        text_height = QFontMetrics(QFont("Arial", 24)).boundingRect(QRect(0, 0, self.width(), self.height()), Qt.TextWordWrap, self.paragraphs[self.current_paragraph]).height()

        self.text_y -= self.text_speed
        if self.text_y < -text_height:
            self.text_y = self.height()
            self.current_paragraph = (self.current_paragraph + 1) % len(self.paragraphs)

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.fillRect(self.rect(), Qt.black)

        painter.setPen(QColor(Qt.yellow))
        font = QFont("Arial", 24)
        painter.setFont(font)

        text_rect = QRect(0, 0, self.width(), self.height())
        bounding_rect = QFontMetrics(font).boundingRect(text_rect, Qt.TextWordWrap, self.paragraphs[self.current_paragraph])

        text_x = (self.width() - bounding_rect.width()) / 2

        painter.drawText(text_x, self.text_y, bounding_rect.width(), bounding_rect.height(), Qt.AlignCenter, self.paragraphs[self.current_paragraph])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MovingTextWidget()
    window.show()
    sys.exit(app.exec())
