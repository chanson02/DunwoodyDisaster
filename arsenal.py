from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QWidget, QGridLayout, QSpacerItem, QSizePolicy, QLayout


class Arsenal(QWidget):
    """
    The arsenal is made up of two `inventory` widgets which display items
    """

    def __init__(self):
        super().__init__()
        self.imageAssets = {
                item: QPixmap(f"./assets/{item}.jpg")
                for item in ["sword", "spear", "shield", "gloves"]
                }

        self.setStyleSheet("background-color: black;")

    def initUI(self):
        try:
            row = 0

            self.main_Lbl = QLabel(self.name)
            self.main_Lbl.setAlignment(Qt.AlignCenter)
            self.main_Lbl.setStyleSheet("color: white;")
            self.mainLayout.addWidget(self.main_Lbl, row, 1)
            row += 1

            self.mainLayout.addItem(
                QSpacerItem(0, 30, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1
            )
            row += 1

            for item in self.contents:
                self.P1_weapon1_Lbl1 = QLabel(item)
                self.P1_weapon1_Lbl1.setAlignment(Qt.AlignCenter)
                self.P1_weapon1_Lbl1.setStyleSheet("color: white;")
                self.mainLayout.addWidget(self.P1_weapon1_Lbl1, row, 1)
                row += 1

                self.mainLayout.addItem(
                    QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1
                )
                row += 1

                self.P1_weapon1_Lbl2 = QLabel("")
                self.P1_weapon1_Lbl2.setAlignment(Qt.AlignCenter)
                self.P1_weapon1_Lbl2.setPixmap(self.imgDict[item])
                self.mainLayout.addWidget(self.P1_weapon1_Lbl2, row, 1)
                row += 1

                self.mainLayout.addItem(
                    QSpacerItem(0, 10, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1
                )
                row += 1

                self.P1_weapon1_Lbl3 = QLabel(
                    "H: "
                    + str(self.contents[item][0])
                    + "\nM: "
                    + str(self.contents[item][1])
                    + "\nMech: "
                    + str(self.contents[item][2])
                )
                self.P1_weapon1_Lbl3.setStyleSheet("color: white;")
                self.mainLayout.addWidget(self.P1_weapon1_Lbl3, row, 1)
                row += 1

                self.mainLayout.addItem(
                    QSpacerItem(0, 40, QSizePolicy.Fixed, QSizePolicy.Fixed), row, 1
                )
                row += 1
        except Exception as e:
            print(e)
