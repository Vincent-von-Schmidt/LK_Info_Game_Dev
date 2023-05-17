import game
import sys
import pygame
from PyQt6.QtWidgets import (
    QWidget,        
    QMainWindow,
    QApplication,
    QVBoxLayout,
)
from PyQt6.QtGui import (
    QPainter,
    QImage,
)
from PyQt6.QtCore import (
    QThreadPool,
)


class PyGame(QWidget):
    def __init__(self, surface: pygame.surface.Surface) -> None:
        super().__init__()

        self.set_surface(surface)

    def set_surface(self, surface: pygame.surface.Surface) -> None:

        self.img: QImage = QImage(
            surface.get_buffer().raw,
            surface.get_width(),
            surface.get_height(),
            QImage.Format.Format_RGB32,
        )

        # self.paintEvent(self.image)

    def paintEvent(self, event) -> None:
        qp = QPainter()
        qp.begin(self)
        qp.drawImage(0, 0, self.image)
        qp.end()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.layout: QVBoxLayout = QVBoxLayout(self)

        self.threadpool = QThreadPool()

        game_main = game.Game(300)
        game_main.signal.surface.connect(self.update)

        self.threadpool.start(game_main)

        self.setLayout(self.layout)

    def update(self, surface: pygame.surface.Surface) -> None:
        img: PyGame = PyGame(surface)
        # img: QImage = QImage(
        #     surface.get_buffer().raw,
        #     surface.get_width(),
        #     surface.get_height(),
        #     QImage.Format.Format_RGB32,
        # )
        self.layout.addWidget(img)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

    # masterSwordsReturn = game.Game(600)
    # masterSwordsReturn.run()
    
