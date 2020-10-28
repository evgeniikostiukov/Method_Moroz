import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QTextEdit, QWidget, QGridLayout, QLabel, QLineEdit
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import time
import datetime
import csv
import os
import seaborn as sns
import pandas as pd

class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent, QtCore.Qt.Window)
        self.build()

    def build(self):
        self.resize(1080, 600) # Задаем размер окна
        self.setWindowTitle('ПЗМР тестирование') # Название окна
        self.figure = plt.figure() # Создание фигуры для графиков
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self) # Панель навигации

        self.firstname = QLineEdit() # Поле ввода имени
        self.lastname = QLineEdit() # Поле ввода фамилии
        self.textEdit = QTextEdit() # Поле информации о тестировании
        self.textEdit.setText('Добро пожаловать в обследование простой зрительно-моторной реакции!'
                              '\n\nДля прохождения тестирования нажмите "Перейти к тестированию". Рекомендуемое количество'
                              ' прохождения тестирования - 3 раза в день.\n\nДля построения графиков нажмите "Построить графики"')
        # Задаем текст поля
        self.textEdit.setReadOnly(True) # Назначаем поле только для чтения

        self.Labelfirstname = QLabel('Введите имя') # Пояснительное поле для имени
        self.Labellastname = QLabel('Введите фамилию') # Пояснительное поле для фамилии

        self.button = QPushButton('Перейти к тестированию') # Создание кнопки перехода к тестированию
        self.buttonClear = QPushButton('Очистить окно') # Создание кнопки очистки окна
        self.buttonPlot = QPushButton('Построить графики') # Создание кнопки построения графиков
        self.button.clicked.connect(self.button_test) # привязываем событие к нажатию кнопки
        self.buttonClear.clicked.connect(self.ClearDialog)
        self.buttonPlot.clicked.connect(self.plot)
        self.grid = QGridLayout() #  создание сетки окна
        # добавление виджетов в сетку
        self.grid.addWidget(self.textEdit, 0, 0)

        self.grid.addWidget(self.Labelfirstname, 1, 0)
        self.grid.addWidget(self.firstname, 1, 1)

        self.grid.addWidget(self.Labellastname, 2, 0)
        self.grid.addWidget(self.lastname, 2, 1)

        self.grid.addWidget(self.button, 4, 0)
        self.grid.addWidget(self.buttonClear, 5, 1)

        self.grid.addWidget(self.canvas, 0, 2, 1, 1)
        self.grid.addWidget(self.toolbar, 1, 2, 1, 1)

        self.grid.addWidget(self.buttonPlot, 4, 1)

        self.setLayout(self.grid)
        self.show()

    def ClearDialog(self): # функция очистки окна
        self.firstname.clear()
        self.lastname.clear()
        self.figure.clear()



    def plot(self): # функция построения графиков
        self.figure.clear()
        self.ax1 = self.figure.add_subplot(111)
        self.df = pd.DataFrame(pd.read_csv('ПЗМР_%s_%s.csv' % (self.firstname.text(), self.lastname.text())))
        print(self.df)
        print(self.df.loc[0, 'V1':'V50'])
        self.mul = pd.MultiIndex.from_frame(self.df)
        print(self.mul)
        self.df = pd.MultiIndex.to_frame(self.mul)
        # df.set_index(['Date', 'Time'])
        print(self.df)
        for self.idx, self.data in self.df.groupby(level=0):
            print('---')
            print(self.data)
            self.ax1 = sns.distplot(self.data.iloc[0, 2:52], label=self.idx, axlabel=False)
            print('AAA', self.data.loc['V1':'V50'])
            # sns.distplot(data.loc[data.iloc[0], 'V1':'V50'], kde=False, axlabel=idx)
        print('DATA0', self.df.loc[self.df.iloc[0], 'V1':'V50'])
        print('DADTA', self.df.iloc[0, 2:52])
        # print('DATA1', df.loc[df.iloc[2], 'V1':'V50'])
        plt.legend()
        plt.xlabel('Время реакции в миллисекундах')
        plt.ylabel('Плотность вероятности')
        self.ax1.set_yticklabels(self.ax1.get_yticks()*1000)
        self.canvas.draw()
        self.show()

    def button_test(self): # функция перехода к окну тестирования
        self.next = Second_window()
        next.__init__()


class Second_window(QWidget): # второе окно
    def __init__(self):
        super().__init__()
        self.build2()

    def build2(self): # функция формирования окна и его виджетов
        self.resize(550, 480)
        self.setWindowTitle('Прохождение теста')
        self.btn1 = QPushButton('Начать тестирование')
        self.btn1.clicked.connect(self.clicked_st)
        self.btn2 = QPushButton('Начать снова')
        self.btn2.clicked.connect(self.clearing)
        self.btn3 = QPushButton('Сохранить результаты')
        self.btn3.clicked.connect(self.saving)
        self.btn4 = QPushButton('Красный')
        self.btn4.clicked.connect(self.clicked_red)
        self.Labelfirstname2 = QLabel('Введите имя')
        self.Labellastname2 = QLabel('Введите фамилию')
        self.Textfirstname2 = QLineEdit()
        self.Textlastname2 = QLineEdit()
        self.Fieldtest = QTextEdit()
        self.Fieldtest.setEnabled(False)
        self.LabelStatus = QLabel('Для начала прохождения тестирования нажмите "Начать тестирование"')
        self.grid2 = QGridLayout()

        self.grid2.addWidget(self.LabelStatus, 1, 1, 1, 2)
        self.grid2.addWidget(self.btn1, 2, 1)
        self.grid2.addWidget(self.btn4, 3, 1)
        self.grid2.addWidget(self.btn2, 4, 1)
        self.grid2.addWidget(self.btn3, 10, 1)
        self.grid2.addWidget(self.Labelfirstname2, 6, 1)
        self.grid2.addWidget(self.Labellastname2, 7, 1)
        self.grid2.addWidget(self.Textfirstname2, 6, 2)
        self.grid2.addWidget(self.Textlastname2, 7, 2)
        self.grid2.addWidget(self.Fieldtest, 2, 2, 4, 2)

        self.setLayout(self.grid2)

        self.show()

        self.result = []
        self.time1 = []
        self.time_res = 0
        self.mistakes = 0

    def clicked_st(self): # функция предъявления стимулов
        self.btn1.setEnabled(False)
        self.seconds = random.uniform(0.5, 2.5)
        self.delta = datetime.timedelta(seconds=self.seconds)
        self.timer = datetime.datetime.now()
        self.timedif = self.timer + self.delta
        self.timedif = self.timedif.second
        print('timer', self.timer, 'd', self.delta, 'dif', self.timedif)
        while self.timer != self.timedif:
            self.timer = datetime.datetime.now().second
            print(self.timer)
        self.Fieldtest.setStyleSheet('Background-color: rgb(255, 0, 0)')
        self.timenow = datetime.datetime.now()
        self.time1.append(self.timenow)

    def clicked_red(self): # функция регистрации реакции на стимулы
        self.timenow = datetime.datetime.now()
        self.Fieldtest.setStyleSheet('Background-color: rgb(255, 255, 255)')
        self.counter = + 1
        self.flag = True
        self.time_res = (self.timenow - self.time1[-1]).total_seconds()
        self.result.append(self.time_res)
        self.LabelStatus.setText('Нажмите старт для продолжения\nВаш результат: %d мс' %(self.time_res * 1000))
        if len(self.result) == 50:
            self.btn1.setEnabled(False)
            self.btn4.setEnabled(False)
            self.LabelStatus.setText("Тест пройден! Не забудьте сохранить результаты")
            print(self.result, 'Кол-во ошибок: ', self.mistakes)
        self.btn1.setEnabled(True)
        if self.time_res < 0.07:
            self.LabelStatus.setText('Ошибка! Слишком рано нажатие.')
            self.Fieldtest.setStyleSheet('Background-color: rgb(255, 255, 0)')
            self.mistakes = + 1
        print(self.result, self.time_res)

    def clearing(self): # функция сброса тестирования
        self.result.clear()
        self.btn1.setEnabled(True)
        self.btn4.setEnabled(True)
        self.LabelStatus.setText("Ваши данные обнулились!")
        self.Textfirstname2.clear()
        self.Textlastname2.clear()
        self.Fieldtest.setStyleSheet('Background-color: rgb(255, 255, 255)')

    def saving(self): # функция сохранения результатов
        self.fname = self.Textfirstname2.text()
        self.lname = self.Textlastname2.text()
        self.date = datetime.datetime.now().date()
        self.timenow = datetime.datetime.now().time()
        self.filename = "ПЗМР_%s_%s.csv" % (self.fname, self.lname)
        self.write_res = []
        with open(self.filename, 'a', newline='') as file:
            self.columns = ["date", "time", "V1", "V2", "V3", "V4", "V5", "V6", "V7", "V8", "V9", "V10", "V11",
                            "V12", "V13", "V14", "V15", "V16", "V17", "V18", "V19", "V20", "V21", "V22", "V23", "V24",
                            "V25", "V26", "V27", "V28", "V29", "V30", "V31", "V32", "V33", "V34", "V35", "V36", "V37",
                            "V38", "V39", "V40", "V41", "V42", "V43", "V44", "V45", "V46", "V47", "V48", "V49", "V50"]
            self.writer = csv.DictWriter(file, fieldnames=self.columns, lineterminator='\n')
            self.write_res.append(['date', self.date.strftime("%x")])
            self.write_res.append(['time', self.timenow.strftime("%X")])
            for i in range(len(self.result)):
                self.write_res.append(['V%d' % (i+1), self.result[i]*1000])
            if os.stat("%s" % self.filename).st_size == 0:
                self.writer.writeheader()
            self.writer.writerow(dict(self.write_res))
            self.LabelStatus.setText("Данные успешно записаны!")
            #self.LabelStatus.setText("Ошибонька!")
            file.close()
        print(self.write_res)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
