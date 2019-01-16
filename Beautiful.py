from bs4 import BeautifulSoup

with open('TIRTH.htm') as fp:
    soup = BeautifulSoup(fp, 'lxml')

questions = soup.findAll('table', {'cellspacing':0, 'cellpadding': 0, 'class':'menu-tbl'})

questions1 = []
for ques in questions:
    q = ques.findAll('td', {'class': 'bold'})
    q1 = []
    for t in q:
        a = t.text
        q1.append(a)
    questions1.append(q1)


class Question:
    def __init__(self, question_id, correct_answer_id, attempt_status, my_answer_id):
        self.question_id = question_id
        self.correct_answer_id = correct_answer_id
        self.attempt_status = attempt_status
        self.my_answer_id = my_answer_id
        self.marks = 0

    def marking(self):
        if self.attempt_status==1:
            if self.correct_answer_id == self.my_answer_id:
                self.marks = 4
            else:
                self.marks = -1
        else:
            pass

question_objects = []
for q in questions1:
    q_id = q[0]
    q_status = q[5]
    q_marked = 0
    if q_status == 'Answered' or q_status == 'Marked For Review':
        q_marked = q[int(q[6])]
    q_obj = Question(q_id, 0, q_status, q_marked)
    question_objects.append(q_obj)



with open('jee.htm') as fp:
    soup = BeautifulSoup(fp, 'lxml')

questions_key = soup.findAll('tr', {'align': 'left'})

question_answers = {}

for q in questions_key[1:91]:
    a = q.findAll('span')
    question_answers.update({a[1].text: a[2].text})

marks = 0
attempt = 0
incorrect = 0
for q in question_objects:
    if q.attempt_status == 'Answered' or q.attempt_status == 'Marked For Review':
        attempt += 1
        if q.my_answer_id == question_answers[q.question_id]:
            print('+4')
            marks += 4
        else:
            print('-1')
            marks = marks - 1
            incorrect += 1
print("MARKS:" + str(marks))
print("Attempted: " + str(attempt))
print("Incorrect: " + str(incorrect))