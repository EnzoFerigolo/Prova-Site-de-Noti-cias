from PySide6.QtWidgets import QDateEdit
from PySide6.QtCore import QDate


class FiltroData(QDateEdit):
    def __init__(self):
        super(FiltroData, self).__init__()

        self.setCalendarPopup(True)
        
        # a API que estou usando só permite notícias de 1 mês atrás 
        self.setDateRange(
            QDate.currentDate().addMonths(-1), QDate.currentDate()
        )
        self.setDate(self.date())

    def getDataSelecionada(self):
        return self.date()
