# -*- coding: utf-8 -*-

import sys


from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QAction, QIcon, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QInputDialog,
    QMainWindow,
    QProgressBar,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QWidget,
    QFileDialog,
    QGroupBox,
    QStatusBar,
    QHBoxLayout,
    QGridLayout

)
from mediaPlayer import Player
import tools as t
import os
import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QLineEdit,
    QMessageBox,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QHBoxLayout

)


class CustomDialog(QDialog):            #создание дилогового окна завершение работы с тестом
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Вы уверены?")        #название окна

        QBtn = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel      # создал 2 кнопки ок и отмена

        self.buttonBox = QDialogButtonBox(QBtn)                 # создани екнопок в окне   
        self.buttonBox.accepted.connect(self.accept)            # кнопка принять
        self.buttonBox.rejected.connect(self.reject)            # кнопка отмены

        self.layout = QVBoxLayout()
        message = QLabel("Завершить тестирование?")             # надпись в окне
        self.layout.addWidget(message)                          # добавление надписи
        self.layout.addWidget(self.buttonBox)                   # добавление кнопок
        self.setLayout(self.layout)




class Testing(QMainWindow):

    question_id = 0
    user_name = ""

    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 1024, 720)  # размер окна
        self.setWindowTitle('Сиситема тестирования: "Проверяйка"')  # название окна

        exit_action = QAction(QIcon('exit.png'), '&Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application') # горячая клавиши выхода
        exit_action.triggered.connect(QApplication.instance().quit)

        open_file = QAction(QIcon('open.png'), 'Open', self)
        open_file.setShortcut('Ctrl+O')  # горячая клавиша открытия файла
        open_file.setStatusTip('Open exam File')
        open_file.triggered.connect(self.showDialog) # подключение к всплывающему окну
        self.menu = self.menuBar()

        file_menu = self.menu.addMenu("&File")  # кнопка чтобы открыть тест
        file_menu.addAction(open_file)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        self.layoutMain = QGridLayout()
        self.open = QPushButton('<< Открыть тест >>', self)
        self.open.clicked.connect(self.showDialog)
        self.open.resize(self.open.sizeHint())
        self.layoutMain.addWidget(self.open, 0,0, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setStatusBar(QStatusBar(self))
        widget = QWidget()
        widget.setLayout(self.layoutMain)
        self.setCentralWidget(widget)

    def showDialog(self):                       # предложениt открыть файл
        self.home_dir = str(os.getcwd())
        self.fname = QFileDialog.getOpenFileName(
            self, 'Открыть файл', self.home_dir)
        self.replay()                           # открытие файла и запуск теста

    def preparerTest(self):
        """
        открыть файл и создать экз. теста
        """
        self.testPath = os.path.split(self.fname[0])[0]
        if self.fname[0]:
            self.EX = t.load_data(self.fname[0])
            self.Result = {}
            self.Score = {}
            for q in range(0, len(self.EX.questions)):
                self.Result[q] = [] #у каждого вопроса нет введенных ответов
                self.Score[q] = 0 # за каждый вопрос дано 0 б.

    def setControl(self):
        self.endTimer()
        self.clear_item(self.layoutControl)
        self.next = QPushButton('Следующий вопрос >>', self)        # кнопка следующего вопроса
        self.next.clicked.connect(self.nextQuestion)
        self.next.resize(self.next.sizeHint())
        self.preview = QPushButton('<< Предыдущий вопрос', self)    # кнопка предыдущего вопроса
        self.preview.clicked.connect(self.previewQuestion)
        self.preview.resize(self.preview.sizeHint())
        self.layoutControl.addWidget(self.preview)
        self.layoutControl.addWidget(self.next)
        self.progressBar.show()
        self.progressBar.setRange(0, self.EX.count_questions()-1)
        self.labelTimer = QLabel(self)
        self.labelTimerDesc = QLabel("Прошло времени: ")        #виджет который показывает сколько времени прошло
        self.timer = QTimer()
        self.timer.timeout.connect(self.showTime)
        self.layoutProgress.addWidget(self.labelTimerDesc, 0, 4)
        self.layoutProgress.addWidget(self.labelTimer, 0, 5, 0, 2)
        self.startTimer()

    def askName(self):                                         # регистрация
        """"
        запрос имени
        """
        text, ok = QInputDialog.getText(
            self, 'Ввод имени', 'Как тебя зовут?',  text=self.user_name)

        if ok:
            if str(text) != "":
                self.user_name = str(text)
            else:
                self.askName()
        else:
            self.askName()

    def testing(self):
        self.questionsFilePath = ""
        self.VideoPlayer = False
        self.VideoPlayerControl = None
        self.AudioPlayerQuestion = False
        self.AudioPlayerQuestionControl = None
        
        self.clear_item(self.layoutPlayerControl)

        if self.question_id <= len(self.EX.questions)-1:
            if self.EX.questions[self.question_id].question_type != "text" and self.EX.questions[self.question_id].path != "":
                self.questionsFilePath = os.path.join(
                    self.testPath, self.EX.questions[self.question_id].question_type, self.EX.questions[self.question_id].path)
            self.clear_item(self.layoutQuestion)

            if self.EX.questions[self.question_id].question != "":
                layout_question_text = QHBoxLayout()
                self.questionText = QLabel(self)
                layout_question_text.addWidget(
                    self.questionText, alignment=Qt.AlignmentFlag.AlignCenter)
                self.questionText.setText(
                    self.EX.questions[self.question_id].question)
                self.layoutQuestion.addLayout(layout_question_text, 0,4,0,3)

            if self.EX.questions[self.question_id].question_type == "image":
                
                layout_question_image = QHBoxLayout()
                self.questionImage = QPixmap(
                    self.questionsFilePath).scaled(500, 500)
                self.questionImageLabel = QLabel()
                self.questionImageLabel.setPixmap(self.questionImage)
                layout_question_image.addWidget(
                    self.questionImageLabel, alignment=Qt.AlignmentFlag.AlignCenter)
                self.layoutQuestion.addLayout(layout_question_image, 1,4,0,3)
            elif self.EX.questions[self.question_id].question_type == "video":
                self.VideoPlayer = True
                self.VideoPlayerControl = Player(
                    self.EX.questions[self.question_id].question_type, stageType="question", file_path=self.questionsFilePath)

                self.layoutQuestion.addWidget(
                    self.VideoPlayerControl.videoWidget, 2,0,5,0 )
                

                self.groupBoxVideoPlayer = QGroupBox(
                    "Управление видео плеером")
                self.layoutQuestion.addWidget(
                    self.groupBoxVideoPlayer, 8,0)
                self.groupBoxVideoPlayer.setLayout(
                    self.VideoPlayerControl.controlLayout)

                # self.layoutQuestion.addLayout(self.VideoPlayerControl.controlLayout)

            elif self.EX.questions[self.question_id].question_type == "audio":
                self.AudioPlayerQuestion = True
                self.AudioPlayerQuestionControl = Player(
                    self.EX.questions[self.question_id].question_type,  stageType="question", file_path=self.questionsFilePath)
                self.layoutQuestion.addLayout(self.AudioPlayerQuestionControl.controlLayout, 2,0,2,11)

            if self.question_id > 0:
                self.preview.setEnabled(True)
            if self.question_id == 0:
                self.preview.setEnabled(False)
            self.clear_item(self.layout_answers)
            self.layout_answers.setContentsMargins(0, 0, 0, 0)
            self.layout_answers.setSpacing(10)
            
            self.AudioPlayerAnswer = False
            self.AudioPlayerAnswerControl = None
            for answers_id in range(0, len(self.EX.questions[self.question_id].answers)):

                if self.EX.questions[self.question_id].answers[answers_id].answer_type != "input":
                    check_box = QCheckBox()
                    check_box.answer = self.EX.questions[self.question_id].answers[answers_id].is_true
                    check_box.id = answers_id
                    check_box.toggled.connect(self.onClicked)
                    if self.EX.questions[self.question_id].answers[answers_id].answer_type == "text":
                        layout_answer = QHBoxLayout()
                        check_box.setText(
                            self.EX.questions[self.question_id].answers[answers_id].answer)
                        layout_answer.addWidget(
                            check_box)
                        self.layout_answers.addLayout(layout_answer)
                    elif self.EX.questions[self.question_id].answers[answers_id].answer_type == "image":
                        layout_answer = QHBoxLayout()
                        layout_answer.addWidget(
                            check_box)
                        answer_file_path = os.path.join(
                            self.testPath, self.EX.questions[self.question_id].answers[answers_id].answer_type, self.EX.questions[self.question_id].answers[answers_id].path)
                        answer_image = QPixmap(
                            answer_file_path).scaled(100, 100)
                        answer_image_label = QLabel()
                        answer_image_label.setPixmap(answer_image)
                        layout_answer.addWidget(
                            answer_image_label)
                        layout_answer.addStretch(1)
                        self.layout_answers.addLayout(layout_answer)
                    elif self.EX.questions[self.question_id].answers[answers_id].answer_type == "audio":
                        self.AudioPlayerAnswer = True
                        layout_answer = QHBoxLayout()
                        layout_answer.addWidget(
                            check_box, alignment=Qt.AlignmentFlag.AlignLeft)

                        play = QPushButton(
                            "Выбрать дорожку для воспроизведения", self)
                        play.id = answers_id
                        play.clicked.connect(self.selectAudioFile)
                        layout_answer.addWidget(play)
                        layout_answer.addStretch(1)
                       # layout_answer.addLayout(player.controlLayout)
                        self.layout_answers.addLayout(layout_answer)
                    if answers_id in self.Result[self.question_id]:
                        check_box.setChecked(True)
                    else:
                        check_box.setChecked(False)
                else:
                    self.input = QLineEdit(
                        placeholderText='Введите ответ...',)
                    self.input.editingFinished.connect(self.updateInput)
                    try:
                        self.input.setText(
                            self.Result[self.question_id][answers_id])
                    except IndexError:
                        self.input.setText("")

                    self.layout_answers.addWidget(self.input)

            if self.AudioPlayerAnswer:
                self.AudioPlayerAnswerControl = Player(
                    "audio", stageType="answer")
                self.groupBoxAudioPlayer = QGroupBox(
                    "Управление аудио плеером")
                self.layoutPlayerControl.addWidget(
                    self.groupBoxAudioPlayer)
                self.groupBoxAudioPlayer.setLayout(
                    self.AudioPlayerAnswerControl.controlLayout)

                # self.layout_answers.addLayout(
                #     self.AudioPlayerControl.controlLayout)

    def selectAudioFile(self):         # выбор аудио файла для конкретного задания
        button = self.sender()
        if self.AudioPlayerAnswer:
            self.AudioPlayerAnswerControl.changeFile(os.path.join(
                self.testPath, "audio", self.EX.questions[self.question_id].answers[button.id].path))
            self.AudioPlayerAnswerControl.play()

    def askEndTest(self):               # вопрос о том хочу я закрыть окно или нет
        dlg = CustomDialog()
        if dlg.exec():
            self.endTest()
        else:
            self.testing()

    def endTest(self):                  # прощальные записи о конце теста
        self.endTimer()
        self.clear_item(self.layoutMain)
        self.UserScore = self.checkResult()
        res = ""
        bal = "Необходимо балов: {0}\nНабрано балов: {1}".format(
            str(self.EX.passingScore), str(self.UserScore))
        if self.UserScore >= self.EX.passingScore:
            res = "Тест пройден!"
        else:
            res = "Тест не пройден!"
        msg = "Участник: {0}\nЗакончил тестирование  по тесту: {1}\nЗа время: {2}\n{3}\nРезультат: {4}".format(
            self.user_name, self.EX.name, str(self.countTimer), bal, res)

        self.questionText = QLabel(self)

        self.questionText.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.questionText.adjustSize()

        self.layoutMain.addWidget(self.questionText, 0,0, alignment=Qt.AlignmentFlag.AlignTop)        # вопрос о том что хочет ли человек повторить тест
        self.questionText.setText(msg)

        self.replayButton = QPushButton('Повторить', self)      
        self.replayButton.clicked.connect(self.replay)
        self.replayButton.resize(self.replayButton.sizeHint())
        self.layoutMain.addWidget(self.replayButton,8,0, alignment=Qt.AlignmentFlag.AlignCenter)

    def replay(self):
        """"
        подготовка осн.окна к работе с вопросом
        """
        self.clear_item(self.layoutMain)
        self.timer = QTimer()
        self.groupBoxQuestion = QGroupBox("Вопрос")
        self.groupBoxAnswers = QGroupBox("Варианты ответов")
        self.layoutQuestion = QGridLayout()
        self.layoutQuestion.setContentsMargins(0, 0, 0, 0)
        self.layoutQuestion.setSpacing(2)
        self.layoutPlayerControl = QHBoxLayout()
        self.layoutPlayerControl.setContentsMargins(0, 0, 0, 0)
        self.layoutPlayerControl.setSpacing(2)
        self.layout_answers = QVBoxLayout()
        self.layout_answers.setContentsMargins(0, 0, 0, 0)
        self.layout_answers.setSpacing(2)
        self.layoutControl = QHBoxLayout()
        self.layoutProgress = QGridLayout()
        self.layoutMain.addWidget(self.groupBoxQuestion, 0,0,5,11 )            # добавляем л.  в основной
        self.groupBoxQuestion.setLayout(self.layoutQuestion)
        self.layoutMain.addLayout(self.layoutPlayerControl, 6,0)
        self.layoutMain.addWidget(self.groupBoxAnswers, 7,0,2,11)
        self.groupBoxAnswers.setLayout(self.layout_answers)
        self.layoutMain.addLayout(self.layoutControl, 9,0)
        self.layoutMain.addLayout(self.layoutProgress, 10,0)
        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.layoutProgress.addWidget(self.progressBar, 0, 0)
        self.askName()
        self.preparerTest()
        self.setControl()
        self.question_id = 0
        self.testing()

    def checkResult(self):
        score = 0
        for question in self.Score:
            score += self.Score[question]
        return score

    def countCorrectAnswerInQuestion(self):
        for answer in self.EX.questions[self.question_id].answers:
            if answer.is_true:
                self.countCorrectAnswer += 1

    def checkAnswer(self):
        """
        Проверка правильности ответа
        """
        # кол-во правильных ответов по тесту
        self.countCorrectAnswer = 0
        self.countCorrectAnswerInQuestion()
        # кол-во правильных ответов пользователя
        self.countCorrectUserAnswer = 0
        # кол-во не правильных ответов пользователя
        self.countIncorrectUserAnswer = 0

        for answers_id in self.Result[self.question_id]:                                # вроде проверка что ответ правильный и зачет того что вопрос уже был и его повторять не  надо
            answers_id = 0 if isinstance(answers_id, str) else answers_id
            if self.EX.questions[self.question_id].answers[answers_id].is_true and self.EX.questions[self.question_id].answers[answers_id].answer_type != "input":
                self.countCorrectUserAnswer += 1
            elif self.EX.questions[self.question_id].answers[answers_id].answer_type == "input":
                if self.EX.questions[self.question_id].answers[answers_id].answer == self.Result[self.question_id][answers_id]:
                    self.countCorrectUserAnswer += 1
            else:
                self.countIncorrectUserAnswer += 1
            self.updateScore()

    def updateScore(self):
        """
        Обновление общего бала self.Score
        """
        if self.countCorrectUserAnswer == self.countCorrectAnswer and self.countIncorrectUserAnswer == 0:
            self.Score[self.question_id] = self.EX.questions[self.question_id].weight
        else:
            self.Score[self.question_id] = 0

    def updateInput(self):
        if self.EX.questions[self.question_id].answers[0].answer_type == "input":
            try:
                self.Result[self.question_id][0] = self.input.text()
            except IndexError:
                self.Result[self.question_id].append(self.input.text())
            print(self.Result[self.question_id])

    def nextQuestion(self):     # функция смена вопроса на следующий 
        if self.VideoPlayer:
            self.VideoPlayerControl.stop()
        if  self.AudioPlayerQuestion:
            self.AudioPlayerQuestionControl.stop()
        if self.AudioPlayerAnswer:
            self.AudioPlayerAnswerControl.stop()
        self.checkAnswer()
        if len(self.EX.questions)-1 <= self.question_id:
            print("last")
            self.testing()
            self.askEndTest()
        else:
            self.question_id += 1
            self.progressBar.setValue(self.question_id)
            self.testing()

    def previewQuestion(self):              # смена вопроса на предыдущий
        if self.VideoPlayer:
            self.VideoPlayerControl.stop()
        if  self.AudioPlayerQuestion:
            self.AudioPlayerQuestionControl.stop()
        if self.AudioPlayerAnswer:
            self.AudioPlayerAnswerControl.stop()
        self.checkAnswer()
        if self.question_id < 0:
            self.question_id = 0
        else:
            self.question_id -= 1
            self.progressBar.setValue(self.question_id)

        self.testing()

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def onClicked(self):
        check_box = self.sender()
        if check_box.isChecked():
            self.Result[self.question_id].append(check_box.id)
        else:
            self.Result[self.question_id].remove(check_box.id)

    def clear_item(self, item):
        """
        очистка лэйаута
        """
        if hasattr(item, "layout"):
            if callable(item.layout):
                layout = item.layout()
        else:
            layout = None
        if hasattr(item, "widget"):
            if callable(item.widget):
                widget = item.widget()
        else:
            widget = None
        if widget:
            widget.setParent(None)
        elif layout:
            for i in reversed(range(layout.count())):
                self.clear_item(layout.itemAt(i))

    def showTime(self):                         # показывает сколько времени прошло с момента начала теста
        self.countTimer += 1
        time_display = str(self.countTimer)
        self.labelTimer.setText(time_display)
        if self.EX.timeLimit != 0 and self.EX.timeLimit == self.countTimer:
            self.endTest()
            reply = QMessageBox()
            reply.setIcon(QMessageBox.Icon.Information)
            reply.setText("Время вышло!")
            reply.setWindowTitle("Превышено время прохождения")
            reply.setStandardButtons(QMessageBox.StandardButton.Ok)
            reply.exec()

    def startTimer(self):           # начало таймера от 0 до 1000 с учетом того что если время вышло то сработает прошлая функция
        self.countTimer = 0
        self.timer.start(1000)

    def endTimer(self):
        """
        функция остановки таймера
        """
        self.timer.stop()


def main():

    app = QApplication(sys.argv)
    ex = Testing()
    ex.show()                                   # запуск программы
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
