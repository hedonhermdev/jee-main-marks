from bs4 import BeautifulSoup

class Question:
    def __init__(self, q_id, options, status, chosen_option):
        self.q_id = q_id
        self.options = options
        self.status = status
        self.chosen_option = chosen_option
        self.chosen_option_id = None

        if self.status == 'Answered' or self.status == 'Marked For Review':
            self.chosen_option_id = self.options[int(self.chosen_option)-1]

with open('tirth.htm') as fp:
    responses = BeautifulSoup(fp, 'lxml').find('div', attrs={'class': 'grp-cntnr'})

questions = []

for question in responses.findAll('table', attrs={'class': 'questionPnlTbl'}):
    question_data = question.find('table', attrs={'class': 'menu-tbl'}).findAll('td')
    q_id = question_data[3].text
    options = [question_data[5].text, question_data[7].text, question_data[9].text, question_data[11].text]
    status = question_data[13].text
    chosen_option = question_data[15].text
    q = Question(q_id, options, status, chosen_option)
    questions.append(q)


with open('jee.htm') as fp:
    answers = BeautifulSoup(fp, 'lxml').find('table', attrs={'class': 'gridv'})

answer_key = {}
for a in answers.findAll('tr')[1:]:
    answer_data = a.findAll('span')
    if len(answer_data) == 3:
        question_id = answer_data[1].text
        answer_id = answer_data[2].text
        answer_key.update({question_id: answer_id})



attempted = 0
correct = 0
incorrect = 0
marks = 0

for q in questions[60: 90]:
    if q.status == 'Answered' or q.status == 'Marked For Review':
        attempted += 1
        if q.chosen_option_id == answer_key[q.q_id]:
            marks += 4
            correct += 1
        else:
            marks = marks - 1
            incorrect += 1
print(attempted)
print(correct, incorrect)
print(marks)
