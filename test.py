import sys, json
from PySide6.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QWidget, QLabel

# from dunwoody_disaster.views.dialogueScreen import DialogueScreen
from dunwoody_disaster.CharacterFactory import CharacterFactory

# from dunwoody_disaster.views.MapScreen import MapScreen
# from dunwoody_disaster.views.FightPreview import FightPreview

# from dunwoody_disaster.views.defeatScreen import DefeatScreen
from dunwoody_disaster import ASSETS
# from dunwoody_disaster.views.CharacterSelector import CharacterSelector
import pygame
import threading
import queue
from PySide6.QtCore import QThread, QTimer
from PySide6.QtGui import QPixmap, QImage
#
#
# def build_test_map():
#     p1 = CharacterFactory.createTestChar()
#     p2 = CharacterFactory.createTestChar()
#     p2.name = "test enemy"
#     ms = MapScreen(p1, None)
#     ms.setAsset("MainMap")
#     ms.addRoom("Bus Stop", (419, 700), p2, "MainMap")
#     ms.addRoom("Court Yard", (693, 559), p2, "no_texture")
#     ms.addRoom("Commons", (451, 449), p2, "no_texture")
#     ms.addRoom("Math", (236, 359), p2, "no_texture")
#     ms.addRoom("English", (770, 366), p2, "no_texture")
#     ms.addRoom("Science", (490, 217), p2, "no_texture")
#     ms.addRoom("Dean's Office", (90, 589), p2, "no_texture")
#     return ms
#
#
# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("test")
#         p1 = CharacterFactory.createTestChar()
#         p2 = CharacterFactory.createTestChar()
#         p2.name = "test enemy"
#         # dls = DialogueScreen(p1, p2)
#         # dls.set_dialogue(["msg 1", "msg2", "msg 3"], ["msg 1", "msg 2", "msg 3"])
#         # self.setCentralWidget(dls)
#
#         # dfs = DefeatScreen()
#         # self.setCentralWidget(dfs)
#
#         # map = build_test_map()
#         # self.setCentralWidget(map)
#         # fight_prev = FightPreview()
#         # fight_prev.set_room(map.rooms[0])
#         # self.setCentralWidget(fight_prev)
#
#         cs = CharacterSelector([p1, p2])
#         self.setCentralWidget(cs)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     mw = MainWindow()
#     mw.show()
#     sys.exit(app.exec())

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.running = True
        self.queue = queue.Queue()
        self.setWindowTitle("test")
        self.label = QLabel('starting')
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.start_pygame()

    def game_loop(self):
        pygame.init()
        screen = pygame.display.set_mode((800, 600))
        clock = pygame.time.Clock()
        iter = 0
        while self.running:
            iter += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            screen.fill((255, 255, 255))
            pygame.draw.circle(screen, (255, 0, 0), (200, 150), 50)
            pygame.display.flip()
            clock.tick(60)

            img_bytes = pygame.image.tobytes(screen, 'RGB')
            #self.queue.put(iter)
            self.queue.put(img_bytes)
        pygame.quit()

    def start_pygame(self):
        self.gthread = threading.Thread(target=self.game_loop)
        self.gthread.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

    def check_queue(self):
        while not self.queue.empty():
            data = self.queue.get()

            img = QImage(data, 800, 600, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(img)
            #print('got ', data)
            #self.label.setText(str(data))
            self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication()
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec())
