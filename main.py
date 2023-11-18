import sqlite3
import sys
import io

from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMainWindow


class AddWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect('coffee.sqlite')
        self.params = {}
        self.pushButton.clicked.connect(self.add_elem)
        self.__is_adding_successful = False
        self.comboBox.addItems(['молотый', 'зерновой'])

    def add_elem(self):
        cur = self.con.cursor()
        try:
            id = cur.execute("SELECT max(id) FROM coffee").fetchone()[0] + 1
            title = self.title.toPlainText()
            roast = self.roast.toPlainText()
            type = self.params.get(self.comboBox.currentText())
            cost = int(self.cost.toPlainText())

            new_data = (id, title, roast, type, '', cost, '1')
            cur.execute("INSERT INTO coffee VALUES (?,?,?,?,?,?,?)", new_data)
            self.__is_adding_successful = True
        except ValueError as ve:
            self.__is_adding_successful = False
            self.statusBar().showMessage("Неверно заполнена форма")
        else:
            self.con.commit()
            self.parent().select()
            self.close()

    def get_adding_verdict(self):
        return self.__is_adding_successful


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee.sqlite")
        self.queryButton.clicked.connect(self.adding)
        self.select()

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

    def adding(self):
        self.add_form = AddWidget(self)
        self.add_form.show()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = except_hook
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())