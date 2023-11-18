import sqlite3
import sys
import io

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.queryButton.clicked.connect(self.select)

    def select(self):
        req = 'SELECT * FROM coffee'
        cur = self.con.cursor()
        result = cur.execute(req).fetchall()
        self.tableWidget.setRowCount(len(result))
        if result:
            self.tableWidget.setColumnCount(len(result[0]))
        else:
            self.tableWidget.setColumnCount(0)
        self.tableWidget.setHorizontalHeaderLabels(
            [i[0] for i in cur.description])
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())