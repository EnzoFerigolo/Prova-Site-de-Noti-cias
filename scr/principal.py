from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QApplication,
    QScrollArea,
    QVBoxLayout,
    QPushButton,
    QLineEdit,
)
import requests
import sys
from variaveis import *
from PySide6.QtCore import Qt
from noticias import Manchete
from filtros import FiltroData
from PySide6.QtGui import QIcon


class TelaPrincipal(QMainWindow):
    def __init__(self) -> None:
        super(TelaPrincipal, self).__init__()
        self.setWindowTitle("Blog do Enzo")
        self.central = QWidget(self)
        self.setCentralWidget(self.central)

        self.gLayout = QGridLayout(self.central)

        self.labelPrincipal = QLabel("Blog Do Enzo - Notícias Diárias", self)
        self.labelPrincipal.setMinimumHeight(self.labelPrincipal.height() + 40)
        self.labelPrincipal.setStyleSheet(
            f"font-size: {XL_FONTE}px; font-family: {FONTE_PRINCIPAL}; text-align: center; font-weight: bold"
        )
        self.labelPrincipal.adjustSize()
        self.gLayout.addWidget(self.labelPrincipal, 0, 0, Qt.AlignmentFlag.AlignCenter)

        self.addFiltros()

        # Criar o QScrollArea como contêiner para as manchetes
        self.areaScroll = QScrollArea(self)
        self.areaScroll.setWidgetResizable(True)

        # Criar um widget para conter as manchetes
        self.scrollWidget = QWidget(self.areaScroll)
        self.sLayout = QVBoxLayout(self.scrollWidget)

        # Adicionar o widget de manchetes ao layout do QScrollArea
        self.areaScroll.setWidget(self.scrollWidget)

        # Adicionar o QScrollArea ao layout principal
        self.gLayout.addWidget(self.areaScroll, 2, 0)

        self.carregarNoticias()
        self.adjustSize()

    def carregarNoticias(self):
        response = requests.get(URL_API)

        print(response)

        if response.status_code == 200:
            artigos = response.json().get("articles", [])

            for artigo in artigos:
                self.sLayout.addWidget(
                    Manchete(
                        artigo["title"],
                        artigo["author"],
                        artigo["publishedAt"],
                        artigo["description"],
                        artigo["url"],
                    ),
                )

        else:
            self.sLayout.addWidget(QLabel("Erro ao obter notícias.", self))

    def carregarNoticiasComFiltro(self):
        dataInicial = self.dataInicial.getDataSelecionada().toString("yyyy-MM-dd")
        dataFinal = self.dataFinal.getDataSelecionada().toString("yyyy-MM-dd")

        response = requests.get(
            f"https://newsapi.org/v2/everything?q={self.inputTexto.text() if self.inputTexto.text() else 'keyword'}&from={dataInicial}&to={dataFinal}&apiKey=5c274943b870497b9b634ac3d55eb5f4"
        )

        for i in reversed(range(self.sLayout.count())):
            self.sLayout.itemAt(i).widget().setParent(None)

        if response.status_code == 200:
            dadosNoticia = response.json()
            artigos = dadosNoticia.get("articles", [])

            if len(artigos):
                for artigo in artigos:
                    self.sLayout.addWidget(
                        Manchete(
                            artigo["title"],
                            artigo["author"],
                            artigo["publishedAt"],
                            artigo["description"],
                            artigo["url"],
                        ),
                    )
            else:
                self.sLayout.addWidget(QLabel("Nenhuma notícia encontrada.", self))

        else:
            self.sLayout.addWidget(QLabel("Erro ao obter notícias.", self))

    # adiciona os inputs de filtros
    def addFiltros(self):
        widget = QWidget(self)
        gLayoutFiltros = QGridLayout(widget)
        widget.setLayout(gLayoutFiltros)

        self.dataInicial = FiltroData()
        gLayoutFiltros.addWidget(self.dataInicial, 0, 0)

        self.dataFinal = FiltroData()
        gLayoutFiltros.addWidget(self.dataFinal, 0, 1)

        self.inputTexto = QLineEdit(widget)
        self.inputTexto.setPlaceholderText("Digite palavra-chave")
        gLayoutFiltros.addWidget(self.inputTexto, 1, 0, 1, 2)

        botaoFiltrar = QPushButton("Filtrar", widget)
        botaoFiltrar.clicked.connect(self.carregarNoticiasComFiltro)
        gLayoutFiltros.addWidget(botaoFiltrar, 2, 0, 2, 2)

        self.gLayout.addWidget(widget, 1, 0, 1, 2)


app = QApplication(sys.argv)
icon = QIcon(SVG)
window = TelaPrincipal()
window.setWindowIcon(icon)  # para Windows
app.setWindowIcon(icon)  # para Mac
window.show()
sys.exit(app.exec())
