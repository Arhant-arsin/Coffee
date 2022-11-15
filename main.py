import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem

from PyQt5 import uic


class MyWidget(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('main.ui', self)
        self.con = sqlite3.connect("coffee")
        self.pb_add.clicked.connect(self.add_field), self.pb_edit.clicked.connect(self.edit_field)
        self.update_result()

    def update_result(self):
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM coffee").fetchall()
        if not result:
            return
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        titles = ('ID', 'Сорт', 'Обжарка', 'Молотость', 'Вкус', 'Цена (рубли)', 'Объем (кг)')
        self.tableWidget.setHorizontalHeaderLabels(titles)

    def add_field(self):
        self.new = addEditCoffee()
        self.new.show()

    def edit_field(self):
        self.new = addEditCoffee(True)
        self.new.show()


class addEditCoffee(QMainWindow):
    def __init__(self, edit=False):
        super().__init__()
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.con = sqlite3.connect("coffee")
        cur = self.con.cursor()
        self.sb_select.valueChanged.connect(self.spin_changed)

    def spin_changed(self):
        cur = self.con.cursor()
        result = cur.execute(f"SELECT * FROM coffee WHERE ID = {self.sb_select.value()}").fetchall()
        if not result:
            result = [('', '', '', '', '', '', '')]
        self.tableWidget.setRowCount(len(result))
        self.tableWidget.setColumnCount(len(result[0]))
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(val)))
        titles = ('ID', 'Сорт', 'Обжарка', 'Молотость', 'Вкус', 'Цена (рубли)', 'Объем (кг)')
        self.tableWidget.setHorizontalHeaderLabels(titles)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec())