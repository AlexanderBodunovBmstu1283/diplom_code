import sys
from PyQt4 import QtGui, QtCore
from parsers import parcer,parcer_by_author,parser_politics,mayak_parcer,sity_parcer
import shutil
import prepare_data
from shutil import copy2
import math
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM, SpatialDropout1D
from keras.datasets import imdb
import os
import re
import random
import subprocess


exited=False

max_features=10000
maxlen=40
sites_list=["http://www.stihi.ru",#0
            "https://rustih.ru",#1
            "https://www.verses.ru",#2
            "http://stihidl.ru",#3
            "http://stih.su",#4
            "https://stihi-russkih-poetov.ru"]#5

class dictionary:
    def __init__(self):
        self.pre_s = []
        with open("pre_changed.txt", "r") as file:
            for line in file:
                line = line.replace("\n", "")
                self.pre_s.append(line)
        self.dict=[]
        with open("common_words.txt","r") as file:
            for i in file:
                self.dict.append(i.replace("\n","").replace("\r",""))

    def __getitem__(self, word,max_features):
        word=self.find_root(word)
        for i in range(len(self.dict)):
            if self.dict[i]==word:
                result=int(self.dict[i-1])
                if result<max_features-1:
                    return int(self.dict[i-1])
                else:
                    return max_features-2
        return max_features-1

    def find_root(self,word):
        word=re.sub(r"[,.!?_()#@$%&*+=/1234567890«»:;]", "", word).replace("А","а").replace("Б","б").replace("В","в").replace("Г","г").replace("Д","д").replace("Е","е").replace("Ж","ж").replace("З","з").replace("И","и").replace("Й","й").replace("К","к").replace("Л","л").replace("М","м").replace("Н","н").replace("О","о").replace("П","п").replace("Р","р").replace("С","с").replace("Т","т").replace("У","у").replace("Ф","ф").replace("Х","х").replace("Ц","ц").replace("Ч","ч").replace("Щ","щ").replace("Ш","ш").replace("Ы","ы").replace("Э","э").replace("Ю","ю").replace("Я","я")

        for i in self.pre_s:
                if (word.startswith(i)):
                    #print(i)#, end="")
                    suspected_root=word[len(i):].zfill(4)[:4].replace("0","")
                    if suspected_root!="0000":
                        return(suspected_root)
        return word.zfill(4)[:4].replace("0","")

    def convert_sentence(self,sentence,max_features):
        words_vector=[]
        for i in sentence.replace("\n"," ").strip().split(" "):
            words_vector.append(self.__getitem__(i,max_features))
        return words_vector

Dict=dictionary()
def extract_train_from_file(file_name,max_features):
    lengts_poems=[]
    result_train=[]
    length_poem=0
    with open(file_name, "r",encoding="utf-8") as file:
        four_rows = ""
        num_rows = 0
        for i in file:
            print(i)
            num_rows += 1
            four_rows += i
            if num_rows == 4:
                length_poem+=1
                result_train.append(Dict.convert_sentence(four_rows, max_features))
                four_rows = ""
                num_rows = 0
    print(result_train)
    return result_train


def activation(x,a):
    return int(x>a)

def classic(x,a):
    if len(x)!= 0:
        g_i=sum(x)/len(x)
    else:
        g_i=0
    Fi=activation(g_i,a)
    return Fi

def harington(x,x1,x2,x3):
    def T(x,x1,x2,x3):
        if x>=0.8:
            return 1
        if x>=0.63:
            return x1
        if x>=0.37:
            return x2
        if x>=0.2:
            return x3
        return 0
    D_i=1
    for j in x:
        f_i_j=math.exp((-1)*math.exp(2-8*j))
        D_i*=f_i_j
        if len(x) != 0:
            D_i=D_i**(1/len(x))
        else:
            D_i=0
        F_i=T(D_i,x1,x2,x3)
    return F_i

def statistics_double(x,a,b):
        if len(x)!=0:
            g_i = sum(activation(j,a) for j in x) / len(x)
        else:
            g_i=0
        Fi = activation(g_i, b)
        return Fi




def get_tags(model):
    arr_tags=[]
    X_recognize=extract_train_from_file("new.txt",10000)
    X_recognize = sequence.pad_sequences(X_recognize, maxlen=maxlen)
    with open("tags_added.txt","r") as file:
        tags=[i.replace("\n","").split(":") for i in file]
    root_dirs=[i[0] for i in tags]
    verbal_categories=[i[1] for i in tags]

    with open ("result.txt","w") as file:
        for i in range(len(root_dirs)):
            model.load_weights("weights/"+root_dirs[i]+"weights.h5")
            print("Веса:", model.weights[0])
            print("Количество объектов для предсказаний", len(X_recognize))
            arr = model.predict(X_recognize)
            arr_new = []
            for j in arr:
                arr_new.append(j[0])
            with open ("params/"+root_dirs[i]+"params.txt","r") as file:
                for string in file:
                    params=string.replace("\n","").split(":")
            params=[int(i) for i in params]
            func=params[0]
            if func==0:
                is_tag=classic(arr_new,params[1]/100)
            if func==1:
                is_tag=harington(arr_new,params[1],params[2],params[3])
            if func==2:
                is_tag=statistics_double(arr_new,params[1]/100,params[2]/100)
            if is_tag==1:
                arr_tags.append(verbal_categories[i])
    return ', '.join(arr_tags)


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setWindowTitle("Интерфейс веб-краулера")
        self.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.adjustSize()

        self.setFixedSize(600,900)  # запрещает изменять размер окна
        self.statusBar()

        self.tab1=QtGui.QTextEdit()
        self.tab2 = QtGui.QTextEdit()
        self.tab3= QtGui.QTextEdit()
        self.tab4 = QtGui.QTextEdit()
        ##################################
        self.vBoxlayout1 = QtGui.QVBoxLayout()
        self.vBoxlayout2 = QtGui.QVBoxLayout()
        self.vBoxlayout3 = QtGui.QVBoxLayout()
        self.vBoxlayout4 = QtGui.QVBoxLayout()
        ##############
        self.TextOutputLinks = QtGui.QTextEdit()
        self.TextOutputLinks.setFixedSize(550, 150)

        self.label1 = QtGui.QLabel()
        self.label1.setFixedSize(550, 30)
        self.label1.setText("Введите адрес страницы категории на сайте:")
        #self.label1.setFont(QtGui.QFont("Times", 20, QtGui.QFont.Bold))

        self.TextInput1Link = QtGui.QLineEdit()
        self.TextInput1Link.setFixedSize(550, 30)

        self.PushButton1 = QtGui.QPushButton()
        self.PushButton1.setFixedSize(550, 50)
        self.PushButton1.setText("Проверить сайт")

        self.TextOutput=QtGui.QTextEdit()
        self.TextOutput.setFixedSize(550, 300)
        ##############

        self.TextOutputLinks2 = QtGui.QTextEdit()
        self.TextOutputLinks2.setFixedSize(550, 150)

        self.label2 = QtGui.QLabel()
        self.label2.setFixedSize(550, 30)
        self.label2.setText("Введите адрес страницы категории на сайте:")

        self.TextInput2 = QtGui.QLineEdit()
        self.TextInput2.setFixedSize(550, 30)

        self.label21 = QtGui.QLabel()
        self.label21.setFixedSize(550, 30)
        self.label21.setText("Введите название категории на РУССКОМ:")

        self.TextInput21 = QtGui.QLineEdit()
        self.TextInput21.setFixedSize(550, 30)

        self.label22 = QtGui.QLabel()
        self.label22.setFixedSize(550, 30)
        self.label22.setText("Введите название категории на АНГЛИЙСКОМ:")

        self.TextInput22 = QtGui.QLineEdit()
        self.TextInput22.setFixedSize(550, 30)

        self.PushButton2 = QtGui.QPushButton()
        self.PushButton2.setFixedSize(550, 50)
        self.PushButton2.setText("Скачать информацию")

        self.TextOutput2 = QtGui.QTextEdit()
        self.TextOutput2.setFixedSize(550, 350)

        self.PushButton21 = QtGui.QPushButton()
        self.PushButton21.setFixedSize(550, 50)
        self.PushButton21.setText("Добавить эту категорию")

        ##############

        self.combo3 = QtGui.QComboBox()
        self.combo3.setEditable(True)
        self.PushButton3 = QtGui.QPushButton()
        self.PushButton3.setFixedSize(550, 50)
        self.TextOutput3 = QtGui.QTextEdit()
        self.TextOutput3.setFixedSize(550, 500)
        ##############
        self.label4 = QtGui.QLabel()
        self.label4.setFixedSize(550, 30)
        self.label4.setText("Выберите категорию, котаая была скачана:")
        self.combo4=QtGui.QComboBox()
        self.combo4.setEditable(True)

        self.PushButton4 = QtGui.QPushButton()
        self.PushButton4.setFixedSize(550, 30)
        self.PushButton4.setText("Сохранить стихотворения на сайт")

        self.TextInput4 = QtGui.QTextEdit()
        self.TextInput4.setFixedSize(550, 600)

        self.TextOutput4 = QtGui.QTextEdit()
        self.TextOutput4.setFixedSize(550, 50)
        ##############
        self.vBoxlayout1.addWidget(self.TextOutputLinks)
        self.vBoxlayout1.addWidget(self.label1)
        self.vBoxlayout1.addWidget(self.TextInput1Link)
        self.vBoxlayout1.addWidget(self.PushButton1)
        self.vBoxlayout1.addWidget(self.TextOutput)
        self.tab1.setLayout(self.vBoxlayout1)
        ##################################
        self.vBoxlayout2.addWidget(self.TextOutputLinks2)
        self.vBoxlayout2.addWidget(self.label2)
        self.vBoxlayout2.addWidget(self.TextInput2)
        self.vBoxlayout2.addWidget(self.label21)
        self.vBoxlayout2.addWidget(self.TextInput21)
        self.vBoxlayout2.addWidget(self.label22)
        self.vBoxlayout2.addWidget(self.TextInput22)
        self.vBoxlayout2.addWidget(self.PushButton2)
        self.vBoxlayout2.addWidget(self.TextOutput2)
        self.vBoxlayout2.addWidget(self.PushButton21)
        self.tab2.setLayout(self.vBoxlayout2)
        ##################################
        self.vBoxlayout3.addWidget(self.combo3)
        self.vBoxlayout3.addWidget(self.PushButton3)
        self.vBoxlayout3.addWidget(self.TextOutput3)
        self.tab3.setLayout(self.vBoxlayout3)
        ##################################
        self.vBoxlayout4.addWidget(self.label4)
        self.vBoxlayout4.addWidget(self.combo4)
        self.vBoxlayout4.addWidget(self.PushButton4)
        self.vBoxlayout4.addWidget(self.TextInput4)
        self.vBoxlayout4.addWidget(self.TextOutput4)
        self.tab4.setLayout(self.vBoxlayout4)
        ##################################
        self.tab_widget = QtGui.QTabWidget()
        self.h_layout = QtGui.QWidget()

        self.tab_widget.addTab(self.tab1, 'Проверить сайт')
        self.tab_widget.addTab(self.tab2, 'Добавление категории')
        #self.tab_widget.addTab(self.tab3, 'Загрузка стихотворений автора')
        self.tab_widget.addTab(self.tab4, 'Загрузка стихотворений на сайт')
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.tab_widget)

        self.summary_box = QtGui.QVBoxLayout()  #
        self.summary_box.addLayout(self.hbox)
        self.h_layout.setLayout(self.summary_box)

        self.setCentralWidget(self.h_layout)
        menubar = self.menuBar()

        self.tags = self.get_tags()
        self.tag_verbal_names = [x[0] for x in self.tags]
        self.root_dirs = [x[1] for x in self.tags]
        self.PushButton1.clicked.connect(self.on_click1)
        self.PushButton2.clicked.connect(self.on_click2)
        self.PushButton21.clicked.connect(self.on_click21)
        self.PushButton3.clicked.connect(self.on_click3)
        self.PushButton4.clicked.connect(self.on_click4)

        self.init_links()
        self.add_names()


    def on_click1(self):
        def check_link(link):
            for i in range(len(sites_list)):
                if link.startswith(sites_list[i]):
                    return i
            return False

        link=self.TextInput1Link.text()
        num=check_link(link)
        if num==0:
            output=parcer.check_poem(parcer.read_poem_links(link))
            string="Заголовок:\n"+str(output[1].encode("cp1252").decode("cp1251")+"\nТекст:\n"+str(output[0].encode("cp1252").decode("cp1251")))
        if num==1:
            output = parcer_by_author.check_poem(parcer_by_author.read_poem_links(link))
            string = "Автор:\n"+str(output[1])+"Заголовок:\n" + str(output[2] + "\nТекст:\n" + str(
                output[0]))
        if num==3:
            output = parser_politics.check_poem(parser_politics.read_poem_links(link))
            string = "Автор:\n" + str(output[1]) + "Заголовок:\n" + str(output[2] + "\nТекст:\n" + str(
                output[0]))

        if num==4:
            output = mayak_parcer.check_poem(mayak_parcer.read_poem_links(link))
            string ="Заголовок:\n" + str(output[1]) + "\nТекст:\n" + str(
                output[0])
        if num==5:
            output = sity_parcer.check_poem(sity_parcer.read_poem_links(link))
            string = "Автор:\n" + str(output[1]) + "Заголовок:\n" + str(output[2] + "\nТекст:\n" + str(
                output[0]))

        self.TextOutput.setText(str(string))

    def on_click2(self):
        def check_link(link):
            for i in range(len(sites_list)):
                if link.startswith(sites_list[i]):
                    return i
            return False
        self.link=self.TextInput2.text()
        self.tag_verbal_name=self.TextInput21.text()
        self.tag_name = self.TextInput22.text()
        num = check_link(self.link)
        if num == 0:
            output = parcer.create_poem_files(parcer.read_poem_links(self.link),self.tag_name)
            string = "Скачано стихотворений:\n"+ str(output[3])+"\nЗаголовок:\n" + str(output[1].encode("cp1252").decode("cp1251") + "\nТекст:\n" + str(
                output[0].encode("cp1252").decode("cp1251")))
        if num==1:
            output = parcer_by_author.create_poem_files(parcer_by_author.read_poem_links(self.link),self.tag_name,'poem_base/')
            string = "Скачано стихотворений:\n"+ str(output[3])+"\nАвтор:\n"+str(output[1])+"Заголовок:\n" + str(output[2] + "\nТекст:\n" + str(
                output[0]))
        with open("tags.txt","a") as file:
            file.write("\n"+self.tag_verbal_name+":"+self.tag_name+":"+self.tag_name+":no_section")
        self.get_tags()

        self.TextOutput2.setText(str(string))


    def on_click21(self):
        prepare_data.write_result_to_files("test_result/","test/",self.tag_name,self.tag_name,10000)
        prepare_data.write_result_to_files("result/","", self.tag_name, self.tag_name, 10000)
        with open("poem_base/" + self.tag_name + "/length_poems.txt", "a+") as file:
            file.write("4,4,6,16,3,3,9,6,4,10")

        self.TextOutput2.setText("Категория готова для обучения")
        self.add_names()






    def on_click3(self):
        pass

    def on_click4(self):
        ##########
        # Создаем сеть
        model = Sequential()
        # Слой для векторного представления слов
        model.add(Embedding(max_features, 32))
        model.add(SpatialDropout1D(0.2))
        # Слой долго-краткосрочной памяти
        model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
        # Полносвязный слой
        # model.add(Dense(glush, activation="sigmoid"))
        model.add(Dense(1, activation="hard_sigmoid"))

        # Копмилируем модель
        model.compile(loss='binary_crossentropy',
                      optimizer='adam',
                      metrics=['accuracy'])
        ##########

        self.index = self.combo4.currentIndex()
        self.root_dir=self.root_dirs[self.index]
        self.tag_verbal_name=self.tag_verbal_names[self.index]
        dir="poem_base/"+self.root_dir+"/"+self.root_dir+"/tags/"
        try:
            os.makedirs(dir)
        except:
            pass
        dir1="poem_base/"+self.root_dir+"/"+self.root_dir+"/texts/"
        num_files = (len(os.listdir(dir1)))
        for i in range (num_files):
            input_poem=""
            copy2(dir1+str(i)+".txt","new.txt")
            tags = get_tags(model)
            self.TextOutput4.setText(tags)
            with open(dir+str(i)+".txt","w", encoding="utf8") as file:
                file.write(tags)
        with open("verbal.txt","w", encoding="utf8")as file:
            file.write(self.tag_verbal_name)
        proc = subprocess.Popen("c:/Python27/python.exe C:/Users/nick/PycharmProjects/mysql_pusher/push_PyQt.py "+self.root_dir,
                                shell=True, stdout=subprocess.PIPE)
        out = proc.stdout.readlines()

    def get_tags(self):
        result=[]
        with open("tags.txt","r") as file:
            for str in file:
                tag_name=str.replace("\n","").split(":")
                result.append(tag_name)
        return result

    def add_names(self):
        for name in self.tag_verbal_names:
            self.combo4.addItem(name)

    def text_ch(self, s):
        name = s
        self.combo2.setEditText(name.capitalize())
        try:
            self.index_cur = self.names.index(name)
        except:
            pass
        else:
            if self.index_cur != self.index_old:
                self.combo.setCurrentIndex(self.index_cur)
            self.index_old = self.index_cur

    def init_links(self):
        self.TextOutputLinks.setText(str('\n'.join(sites_list)))
        self.TextOutputLinks2.setText(str('\n'.join(sites_list)))


def stop_():
    global exited
    exited = True


def appExec():
  app = QtGui.QApplication(sys.argv)
  # and so on until we reach:
  main_window = MainWindow()
  main_window.show()
  app.exec_()
  # other work...


if exited==False:
    sys.exit(appExec())
