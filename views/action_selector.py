from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLayout, QGridLayout


class ActionSelector(QWidget):
    def __init__(self):
        super().__init__()
        self.player = None  # TODO

        self.default_widget = self.create_default_widget()
        self.fight_widget = self.create_fight_widget()
        self.fight_widget.hide()

        layout = QHBoxLayout()
        layout.addWidget(self.default_widget)
        layout.addWidget(self.fight_widget)
        self.setLayout(layout)

    def create_default_widget(self) -> QWidget:
        layout = QHBoxLayout()

        fight_btn = QPushButton('Fight')
        fight_btn.clicked.connect(self.selectedFight)
        layout.addWidget(fight_btn)

        items_btn = QPushButton('Items')
        # items_btn.clicked.connect(self.selectedItems)
        layout.addWidget(items_btn)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def create_fight_widget(self) -> QWidget:
        layout = QGridLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # moves = self.player.moves  # TODO
        moves = []
        for i, move in enumerate(moves):
            row = i // 2
            col = i % 2
            btn = QPushButton(move)
            layout.addWidget(btn, row, col)

        back_btn = QPushButton('Back')
        back_btn.clicked.connect(self.selectedBack)
        layout.addWidget(back_btn, len(moves) // 2 + 1, 0)

        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def selectedFight(self):
        self.default_widget.hide()
        self.fight_widget.show()
        return

    def selectedBack(self):
        self.default_widget.show()
        self.fight_widget.hide()
        return
