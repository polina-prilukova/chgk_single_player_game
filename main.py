import sys
from PyQt5 import QtWidgets, QtCore, QtGui
# import design
import design_2
import Parser


class ExampleApp(QtWidgets.QMainWindow, design_2.Ui_MainWindow):

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.q_pack = []

        self.timer_running = False
        self.timer_seconds = 60
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.show_timer)

        # self.question_frame.setVisible(False)
        # self.answer_frame.setVisible(False)
        # self.result_frame.setVisible(False)
        # self.control_frame.setVisible(False)

        self.start_btn.clicked.connect(self.start_game)
        self.previous_btn.clicked.connect(self.show_previous_question)
        self.next_btn.clicked.connect(self.show_next_question)
        self.show_answer_btn.clicked.connect(self.show_answer)
        self.pause_btn.clicked.connect(self.timer_start_pause)

        self.is_answered_checkBox.stateChanged.connect(self.state_changed)

        self.previous_btn.setToolTip('Предыдущий вопрос')
        self.next_btn.setToolTip('Следующий вопрос')
        self.pause_btn.setToolTip('Пауза/продолжить')

    def show_timer(self):
        pal = self.timer_label.palette()

        if self.timer_seconds >= 0:
            if self.timer_seconds <= 10:
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("red"))
            else:
                pal.setColor(QtGui.QPalette.WindowText, QtGui.QColor("black"))
            self.timer_label.setPalette(pal)
            self.timer_label.setText(str(self.timer_seconds))
            self.timer_seconds -= 1

        if self.timer_seconds == -1:
            self.show_answer()

    def timer_start_pause(self):
        self.timer_running = not self.timer_running
        if self.timer_running:
            self.timer.start(1000)
        else:
            self.timer.stop()

    def timer_reset(self):
        self.timer_running = False
        self.timer.stop()
        self.timer_seconds = 60
        self.timer_label.setText('')
        # self.show_timer()


    def state_changed(self):
        if self.is_answered_checkBox.isChecked():
            self.q_pack.question_list[self.q_pack.current_question].is_answered = True
        else:
            self.q_pack.question_list[self.q_pack.current_question].is_answered = False
        t_number, q_number = Parser.get_tour_number_and_question_number(
            self.q_pack.question_list[self.q_pack.current_question].number)
        if q_number == 0:
            return
        t_index = t_number - 1
        # q_index = int(q_number - 1) % self.results_table.rowCount()
        q_index = int(q_number - 1) % self.results_table.columnCount()
        if self.is_answered_checkBox.isChecked():
            self.results_table.item(t_index, q_index).setText('+')
        else:
            self.results_table.item(t_index, q_index).setText('-')

    def create_results_table(self):
        # TODO проверить https://db.chgk.info/tour/zemli20.3_u выводится таблица 4*9 вместо 3*12
        tours_number = int(max(set([x.number.split('-')[0] for x in self.q_pack.question_list])))
        questions_in_tour = int(len(self.q_pack.question_list)/tours_number)

        # self.results_table.setColumnCount(tours_number)
        # self.results_table.setRowCount(questions_in_tour)
        self.results_table.setColumnCount(questions_in_tour)
        self.results_table.setRowCount(tours_number)
        self.results_table.resizeColumnsToContents()
        self.results_table.resizeRowsToContents()
        # for tour in range(0, tours_number):
        #     for question in range(0, questions_in_tour):
        for question in range(0, questions_in_tour):
            for tour in range(0, tours_number):
                item = QtWidgets.QTableWidgetItem()
                item.setText('-')
                self.results_table.setItem(tour,question, item)

    def show_question(self, current_question):
        t_number, q_number = Parser.get_tour_number_and_question_number(current_question.number)
        self.question_textEdit.setStyleSheet("fontName=Times-Bold")
        self.question_textEdit.append('Вопрос №' + str(q_number) + ':')
        self.question_textEdit.setStyleSheet("fontName=Times")
        self.question_textEdit.append(current_question.question_text)
        self.is_answered_checkBox.setChecked(current_question.is_answered)

    def show_answer(self):
        self.timer.stop()
        current_question = self.q_pack.question_list[self.q_pack.current_question]
        self.answer_textEdit.append('Ответ: ' + current_question.answer)
        if current_question.pass_criteria:
            self.answer_textEdit.append('Зачет: ' + current_question.pass_criteria)
        if current_question.comments:
            self.answer_textEdit.append('Комментарий: ' + current_question.comments)
        if current_question.sources:
            self.answer_textEdit.append('Источник: ' + current_question.sources)
        # TODO в базе автор может быть ссылкой. В этом случае текст ФИО не выводится, исправить
        # if current_question.author:
        #     self.answer_textEdit.append('Автор: ' + current_question.author)

    def check_first_last_questions(self):
        if self.q_pack.current_question == 0:
            self.previous_btn.setEnabled(False)
        else:
            self.previous_btn.setEnabled(True)
        if self.q_pack.current_question == len(self.q_pack.question_list) - 1:
            self.next_btn.setEnabled(False)
        else:
            self.next_btn.setEnabled(True)

    def show_previous_question(self):
        self.timer_reset()
        self.question_textEdit.clear()
        self.answer_textEdit.clear()
        self.q_pack.current_question -= 1
        self.show_question(self.q_pack.question_list[self.q_pack.current_question])
        self.check_first_last_questions()

    def show_next_question(self):
        self.timer_reset()
        self.question_textEdit.clear()
        self.answer_textEdit.clear()
        self.q_pack.current_question += 1
        self.show_question(self.q_pack.question_list[self.q_pack.current_question])
        self.check_first_last_questions()

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
