from bs4 import BeautifulSoup, NavigableString
import requests
import re


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

    def find_tag_by_class_and_fill_question(self, class_name, attribute_name):
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


# headers = requests.utils.default_headers()
# headers.update({'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})

url = "https://db.chgk.info/tour/ligavuz19.1_u"
req = requests.get(url)
soup = BeautifulSoup(req.content, 'html.parser')

counter = 0

id_question_header = url.split('/')[-1]

package = []

# для источника db.chgk.info
# поиск нужных тегов с html-страницы
for tag in soup.find_all('div', attrs={'class': 'question'}):
    new_question = Question_chgk()
    new_question.number = tag['id'].replace(id_question_header + '.', '')

    # TODO обработка изображений - раздаточных материалов
    new_question.find_tag_by_class_and_fill_question('Question', 'question_text')
    new_question.find_tag_by_class_and_fill_question('Answer', 'answer')
    new_question.find_tag_by_class_and_fill_question('PassCriteria', 'pass_criteria')
    new_question.find_tag_by_class_and_fill_question('Comments', 'comments')
    new_question.find_tag_by_class_and_fill_question('Sources', 'sources')
    new_question.find_tag_by_class_and_fill_question('Authors', 'author')

    # new_question.remove_spaces()

    package.append(new_question)

# проверим, что пакет корректный. Т.е. у всех вопросов пакета как минимум есть вопрос и есть ответ
is_correct = True
error_string = ''
for question in package:
    if not question.question_text:
        error_string += f'Вопрос №{question.number} не содержит вопроса \n'
        is_correct = False
    if not question.answer:
        error_string = f'Вопрос №{question.number} не содержит ответа \n'
        is_correct = False

if not is_correct:
    error_string += 'Пакет не корректный, проверьте выгрузку'
    print(error_string)

# запишем полученные данные в файл
with open('test.txt', 'w', encoding='UTF-8') as f:
    f.write(soup.title.text)
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





