import sys

from PySide6.QtWidgets import *

if __name__ == "__main__":
    app = QApplication()

    botao = QPushButton("Texto do botao")
    botao.show()

    app.exec()
