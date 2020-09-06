import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
import design
import Parser
import numpy as np
from functools import partial
from Parser import Question_chgk, Package_chgk


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class ExampleApp(QtWidgets.QMainWindow, design.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.q_pack = []
        self.model = TableModel([])

        self.question_frame.setVisible(False)
        self.answer_frame.setVisible(False)
        self.result_frame.setVisible(False)
        self.control_frame.setVisible(False)

        self.start_btn.clicked.connect(self.start_game)
        self.previous_btn.clicked.connect(self.show_previous_question)
        self.next_btn.clicked.connect(self.show_next_question)

        self.previous_btn.setToolTip('Предыдущий вопрос')
        self.next_btn.setToolTip('Следующий вопрос')
        self.pause_btn.setToolTip('Пауза/продолжить')

    def create_results_table(self):
        tours_number = int(max(set([x.number.split('-')[0] for x in self.q_pack.question_list])))
        questions_in_tour = int(len(self.q_pack.question_list)/tours_number)
        data = np.zeros(len(self.q_pack.question_list))
        data = data.reshape(questions_in_tour, tours_number)
        self.model = TableModel(data)
        self.results_tableView.setModel(self.model)
        self.results_tableView.resizeColumnsToContents()
        self.results_tableView.resizeRowsToContents()

    def show_question(self, current_question):
        t_number, q_number = Parser.define_tour_number_and_question_number(current_question.number)
        self.question_textEdit.setStyleSheet("fontName=Times-Bold")
        self.question_textEdit.append('Вопрос №' + q_number + ':')
        self.question_textEdit.setStyleSheet("fontName=Times")
        self.question_textEdit.append(current_question.question_text)

    def show_previous_question(self):
        self.question_textEdit.clear()
        self.q_pack.current_question -= 1
        self.show_question(self.q_pack.question_list[self.q_pack.current_question])

    def show_next_question(self):
        self.question_textEdit.clear()
        self.q_pack.current_question += 1
        self.show_question(self.q_pack.question_list[self.q_pack.current_question])

    def start_game(self):
        if not self.url_lineEdit.text():
            self.question_textEdit.setText("Введите ссылку")
            self.url_lineEdit.setFocus()
        else:
            pack = Parser.parse_url(url=self.url_lineEdit.text().strip())
            self.q_pack = pack

            self.question_frame.setVisible(True)
            self.answer_frame.setVisible(True)
            self.result_frame.setVisible(True)
            self.control_frame.setVisible(True)

            self.create_results_table()

            try:
                self.show_question(self.q_pack.question_list[self.q_pack.current_question])

            except:
                self.question_textEdit.setText("Что-то не так")


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = ExampleApp()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()
