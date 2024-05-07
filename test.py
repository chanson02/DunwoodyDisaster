import sys
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PySide6.QtCore import QTimer, Qt

class TypewriterEffectWidget(QWidget):
    def __init__(self, text, interval=100):
        super().__init__()
        self.text = text
        self.interval = interval
        self.label = QLabel("")
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        self.label.setWordWrap(True)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.add_char)
        self.char_index = 0

        self.timer.start(self.interval)

    def add_char(self):
        if self.char_index < len(self.text):
            current_text = self.label.text()
            current_text += self.text[self.char_index]
            self.label.setText(current_text)
            self.char_index += 1
        else:
            self.timer.stop()  # Stop the timer if the text is complete

if __name__ == "__main__":
    app = QApplication(sys.argv)
    text = "Hello, this is text appearing as if it's being typed!"
    widget = TypewriterEffectWidget(text, 50)  # Adjust interval for speed
    widget.resize(400, 100)
    widget.show()
    sys.exit(app.exec())
