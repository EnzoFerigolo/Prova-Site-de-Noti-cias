from PySide6.QtWidgets import QWidget, QGridLayout, QLabel
from PySide6.QtCore import Qt, QUrl, Signal
from PySide6.QtGui import QDesktopServices, QMouseEvent
from variaveis import *
import datetime


class ClickableLabel(QLabel):
    clicked = Signal()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.clicked.emit()


class Manchete(QWidget):
    def __init__(self, titulo, autor, publicado, descricao, link) -> None:
        super().__init__()

        self.gLayout = QGridLayout()
        self.setLayout(self.gLayout)

        self.titulo = ClickableLabel(titulo, self)
        self.titulo.setWordWrap(True)
        self.titulo.setMinimumHeight(self.titulo.height() * 3 + 12)
        self.titulo.setStyleSheet(
            f"font-family: {FONTE_PRINCIPAL}; font-size: {L_FONTE}px"
        )

        if link:
            self.link = link
            self.titulo.setCursor(Qt.PointingHandCursor)  # type: ignore
            self.titulo.clicked.connect(self.abrirPagina)

        self.gLayout.addWidget(self.titulo, 0, 0, Qt.AlignmentFlag.AlignLeft)

        if autor:
            self.autor = QLabel(autor, self)
            self.autor.setStyleSheet(
                f"font-family: {FONTE_SECUNDARIA}; font-size: {S_FONTE}px"
            )
            self.gLayout.addWidget(self.autor, 2, 0, Qt.AlignmentFlag.AlignLeft)

        if publicado:
            self.data = QLabel(
                str(
                    datetime.datetime(
                        int(publicado[:4]), int(publicado[5:7]), int(publicado[8:10])
                    )
                )[:10],
                self,
            )
            self.data.setStyleSheet(
                f"color: {PRIMARIA}; font-size: {XS_FONTE}; font-family: {FONTE_SECUNDARIA}"
            )
            self.gLayout.addWidget(self.data, 2, 0, Qt.AlignmentFlag.AlignRight)

        if descricao:
            self.descricao = QLabel(descricao, self)
            self.descricao.setMinimumHeight(self.descricao.height() * 2)
            self.data.setStyleSheet(
                f"color: {PRIMARIA}; font-size: {S_FONTE}; font-family: {FONTE_SECUNDARIA}"
            )
            self.descricao.setWordWrap(True)
            self.descricao.adjustSize()
            self.gLayout.addWidget(
                self.descricao, 1, 0, 1, 2, Qt.AlignmentFlag.AlignLeft
            )

        self.setMinimumWidth(self.titulo.width())
        self.setMaximumWidth(self.width())
        self.setMaximumHeight(self.height())
        self.adjustSize()

    pass

    def abrirPagina(self):
        QDesktopServices.openUrl(QUrl(self.link))
