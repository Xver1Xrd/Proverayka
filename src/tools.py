# -*- coding: utf-8 -*-

import yaml
import random

global globalList
globalList = []


class Answer:
    def __init__(self, is_true: bool, answer_type: str, answer: str, path: str):
        self._answer = answer  # ответ
        self._answer_type = answer_type  # тип ответа
        self._is_true = is_true  # правильный?
        self._path = path

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = val

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, val):
        self._answer = val

    @property
    def answer_type(self):
        return self._answer_type

    @answer_type.setter
    def answer_type(self, val):
        self._answer_type = val

    @property
    def is_true(self):
        return self._is_true

    @is_true.setter
    def is_true(self, val):
        self._is_true = val


class Question:
    def __init__(self, question: str, question_type: str, answers: list, path: str):
        self._question = question  # вопрос
        self._question_type = question_type  # тип вопроса
        self._answers = globalList + answers  # ответы
        self._path = path  # путь к вопросу
        self._weight = 1  # вес вопроса

    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, val):
        self._weight = val

    @property
    def question(self):
        return self._question

    @question.setter
    def question(self, val):
        self._question = val

    @property
    def question_type(self):
        return self._question_type

    @question_type.setter
    def question_type(self, val):
        self._question_type = val

    @property
    def answers(self):
        return self._answers

    @answers.setter
    def answers(self, val):
        self._answers = val

    def append(self, val):
        self.answers = self.answers + [val]
        return self.answers

    def extend(self, val):
        return self.answers.extend(val)

    def count_answers(self):
        return len(self.answers)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, val):
        self._path = val


class Exam:
    def __init__(self, name: str, passingScore: int):
        self._name = name
        self._questions = []
        self._questionID = 0
        self._timeLimit = 0 
        self._passingScore = passingScore  # проходной бал

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, val):
        self._description = val

    @property
    def version(self):
        return self._version

    @version.setter
    def version(self, val):
        self._version = val

    @property
    def timeLimit(self):
        return self._timeLimit

    @timeLimit.setter
    def timeLimit(self, val):
        self._timeLimit = val

    @property
    def passingScore(self):
        return self._passingScore

    @passingScore.setter
    def passingScore(self, val):
        self._passingScore = val

    @property
    def questionID(self):
        return self._questionID

    @questionID.setter
    def questionID(self, questionID: int):
        self._questionID = questionID

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    def count_questions(self):
        return len(self._questions)

    def get_question(self, id: int) -> Question:
        return self._questions[id]

    @property
    def questions(self):
        return self._questions

    @questions.setter
    def questions(self, val: Question):
        self._questions = val

    def append(self, val: Question):
        self.questions = self.questions + [val]
        return self.questions

    @questions.deleter
    def questions(self):
        self._questions.clear()

    def remove(self, f: Question):
        self._questions.remove(f)


def load_data(file: str) -> Exam:

    with open(file, "rb") as import_exam:
        try:
            data = yaml.safe_load(import_exam)

            ex = Exam(data["name"], data["passingScore"])
            # ex.name = data["name"]
            # ex.passingScore = data["passingScore"]  # проходной бал
            if "timeLimit" in data.keys():
                ex.timeLimit = data["timeLimit"]  # лимит времени

            if "description" in data.keys():
                ex.description = data["description"]
            if "version" in data.keys():
                ex.version = data["version"]
            for q in data["questions"]:
                answers = []
                for a in q["answers"]:
                    answerText = ""
                    answerPath = ""
                    if "answer" in a.keys():
                        answerText = a["answer"]
                    if "path" in a.keys():
                        answerPath = a["path"]
                    answer = Answer(
                        a["isTrue"], a["answerType"], answerText, answerPath)
                    answers.append(answer)
                questionText = ""
                if "question" in q.keys():
                    questionText = q["question"]
                random.shuffle(answers)
                questionPath = ""
                if "path" in q.keys():
                    questionPath = q["path"]
                question = Question(
                    questionText, q["questionType"], answers, questionPath)
                if "weight" in q.keys():
                    question.weight = q["weight"]
                ex.append(question)
            print(ex.name)
            random.shuffle(ex.questions)
            return ex
        except yaml.YAMLError as exc:
            print(exc)
            return exc


# if __name__ == "__main__":
def run(ex: Exam):
    # ex = load_data("test.yml")
    # print(ex.name)
    count = 0
    for q in ex.questions:
        ad = q.answers
        print(q.question)
        print("***********************************")
        for a in ad:
            print(a.answer)

        # q.user_answer = [int(x) for x in input().split()]
        print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")


if __name__ == "__main__":
    ex = load_data("test.yml")
    run(ex)
