from bs4 import BeautifulSoup, NavigableString
import requests
import re


class Package_chgk(object):
    def __init__(self):
        self.title = ''
        self.question_list = []
        self.date = ''
        self.correctors = ''
        self.current_question = 0


class Question_chgk(object):
    # def __init__(self, number, question_text, answer, pass_criteria, comments, sources, author):
    def __init__(self):
        self.number = ''
        self.question_text = ''
        self.answer = ''
        self.pass_criteria = ''
        self.comments = ''
        self.sources = ''
        self.author = ''
        self.is_answered = False

    def find_tag_by_class_and_fill_question(self, class_name, attribute_name, tag):
        new_tag = tag.find('strong', attrs={'class': class_name})
        if new_tag:
            for new_str in new_tag.next_siblings:
                if isinstance(new_str, str):
                    if attribute_name == 'question_text':
                        self.question_text += new_str.strip() + '\n'
                    elif attribute_name == 'answer':
                        self.answer += new_str.strip()
                    elif attribute_name == 'pass_criteria':
                        self.pass_criteria += new_str.strip()
                    elif attribute_name == 'comments':
                        self.comments += new_str.strip()
                    elif attribute_name == 'sources':
                        self.sources += new_str.strip()
                    elif attribute_name == 'author':
                        self.author += new_str.strip()


class Game(object):
    def __init__(self):
        self.is_on = True

def get_tour_number_and_question_number(question_number):
    t_number, q_number = question_number.split('-')
    return int(t_number), int(q_number)


def check_if_package_correct(package):
    # проверим, что пакет корректный. Т.е. у всех вопросов пакета как минимум есть вопрос и есть ответ
    is_correct = True
    error_string = ''
    for q in package:
        if not q.question_text:
            error_string += f'Вопрос №{q.number} не содержит вопроса \n'
            is_correct = False
        if not q.answer:
            error_string = f'Вопрос №{q.number} не содержит ответа \n'
            is_correct = False

    if not is_correct:
        error_string += 'Пакет не корректный, проверьте выгрузку'
        print(error_string)


def parse_url(url):
    # url = "https://db.chgk.info/tour/ligavuz19.1_u"
    # headers = requests.utils.default_headers()
    # headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'html.parser')

    id_question_header = url.split('/')[-1]

    pack = Package_chgk()

    # для источника db.chgk.info
    # поиск нужных тегов с html-страницы
    for tag in soup.find_all('div', attrs={'class': 'question'}):
        new_question = Question_chgk()
        new_question.number = tag['id'].replace(id_question_header + '.', '')

        # TODO обработка изображений - раздаточных материалов
        new_question.find_tag_by_class_and_fill_question('Question', 'question_text', tag)
        new_question.find_tag_by_class_and_fill_question('Answer', 'answer', tag)
        new_question.find_tag_by_class_and_fill_question('PassCriteria', 'pass_criteria', tag)
        new_question.find_tag_by_class_and_fill_question('Comments', 'comments', tag)
        new_question.find_tag_by_class_and_fill_question('Sources', 'sources', tag)
        new_question.find_tag_by_class_and_fill_question('Authors', 'author', tag)

        pack.question_list.append(new_question)

    # check_if_package_correct(pack.question_list)
    return pack


def write_package_to_txt(package):
    # запишем полученные данные в файл
    with open('test.txt', 'w', encoding='UTF-8') as f:
        # f.write(soup.title.text)
        f.write('\n')
        for question in package:
            f.write('Вопрос №' + question.number + ':')
            f.write('\n')
            f.write(question.question_text)
            f.write('\n')
            f.write('Ответ: ')
            f.write(question.answer)
            f.write('\n')
            if question.pass_criteria:
                f.write('Зачет: ')
                f.write(question.pass_criteria)
                f.write('\n')
            if question.comments:
                f.write('Комментарий: ')
                f.write(question.comments)
                f.write('\n')
            if question.sources:
                f.write('Источник: ')
                f.write(question.sources)
                f.write('\n')
            if question.author:
                f.write('Автор: ')
                f.write(question.author)
                f.write('\n')

            f.write('\n')
        f.close()
    print('Файл записан')
