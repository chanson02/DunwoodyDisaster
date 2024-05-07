from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
import dunwoody_disaster as DD


class CooperIntroScreen(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()
        self.setLayout(layout)

        text = """
        Meet Cooper, the {tbd} programmer!
        Even though he's not the best with his hands, he loves to build things.
        Especially keyboards and cars.
        Join him on his epic adventure through Dunwoody College of Techology
        where he will encounter many hardships on his path to a righteous Software Engineering degree.
        """

        lbl = QLabel(" ".join(text.replace("\n", " ").split()))
        lbl.setWordWrap(True)
        layout.addWidget(lbl)
