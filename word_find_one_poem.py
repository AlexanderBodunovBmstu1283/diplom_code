#!/usr/bin/python
# -*- coding: cp1251 -*-
#import mysql_connect
import re
import os
import numpy as np
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Activation, Embedding
from keras.layers import LSTM, SpatialDropout1D
from keras.datasets import imdb
import os
import random
from collections import deque
import matplotlib.pyplot as plt
import sys
from PyQt4 import QtGui, QtCore
import math

maxlen=40
max_features = 10000
#num_sets=[13,5,15,8,10,6,11,1]
#root_dirs=["light","fentezi_realism",#0,1
#            "filosofic_light","humor_serious",#2,3
 #           "military","mistics","nostalgic",#4,5,6
 #           "office_home","patriotic",#7,8
 #           "piece_revolution","politics",#9,10
 #           "religion_ateistic","sity_village",#11,12
 #           "to_child","to_female_to_male","lirics"]#13,14,15

#verbal_categories=["для детей","сюр","лирические","патриотические","о политике","память о юности","религиозные","фентези"]

def activation(x,a):
    return int(x>a)

def classic(x,a):
    g_i=sum(x)/len(x)
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
        D_i=D_i**(1/len(x))
        F_i=T(D_i,x1,x2,x3)
    return F_i

def statistics_double(x,a,b):
        g_i = sum(activation(j,a) for j in x) / len(x)
        Fi = activation(g_i, b)
        return Fi



def recognize(model, root_dir, section_dir):
    def activation(x, a):
        return int(x > a)

    def error_value(F, A):
        sum = 0
        for i in range(len(F)):
            sum += abs(F[i] - A[i])
        print("Количество ошибок = ", sum)
        return sum

    def classic(x, a):
        result = []
        for i in x:
            g_i = sum(i) / len(i)
            Fi = activation(g_i, a)
            result.append(Fi)
        return result

    def harington(x, x1, x2, x3):
        def T(x, x1, x2, x3):
            if x >= 0.8:
                return 1
            if x >= 0.63:
                return x1
            if x >= 0.37:
                return x2
            if x >= 0.2:
                return x3
            return 0

        result = []
        for i in x:
            D_i = 1
            for j in i:
                f_i_j = math.exp((-1) * math.exp(2 - 8 * j))
                D_i *= f_i_j
            D_i = D_i ** (1 / len(i))
            F_i = T(D_i, x1, x2, x3)
            result.append(F_i)
        return result

    def statistics_double(x, a, b):
        result = []
        for i in x:
            g_i = sum(activation(j, a) for j in i) / len(i)
            Fi = activation(g_i, b)
            result.append(Fi)
        return result

    def calculate_params(x, a, i):
        min_error=20
        params=[0]
        if i == 1:
            for a in range(0, 100):
                Fi = classic(x, a / 100)
                # print (Fi)
                num_errors = error_value(Fi, A)
                print(num_errors)
                if num_errors<min_error:
                    min_error=num_errors
                    params = [a]

        if i == 2:
            for x1 in range(0, 2):
                for x2 in range(0, 2):
                    for x3 in range(0, 2):
                        if x1 >= x2 >= x3:
                            Fi = harington(x, x1, x2, x3)
                            num_errors = error_value(Fi, A)
                            print(num_errors)
                            if num_errors < min_error:
                                min_error = num_errors
                                params = [x1,x2,x3]
        if i == 3:
            for a in range(0, 100):
                for b in range(0, 100):
                    Fi = statistics_double(x, a / 100, b / 100)
                    num_errors = error_value(Fi, A)
                    if num_errors < 7:
                        print(a / 100, " ", b / 100, " ", num_errors)
                        if num_errors < min_error:
                            min_error = num_errors
                            params = [a,b]
                        if num_errors==0:
                            return [min_error, params]
        return [min_error,params]

    set_for_recognize = load_data_mixer(root_dir, section_dir, "test")
    with open ("poem_base/"+root_dir+"/length_poems.txt","r") as file:
        for string in file:
            final_string=string.replace("\n","")

    X_recognize = set_for_recognize[0]  # [[12,max_features-glush,14,111,14],[14,67,86,12],[134,64,86,32]]
    Z_recognize = final_string.split(",")
    Z_recognize=[int(x) for x in Z_recognize]

    X_recognize = sequence.pad_sequences(X_recognize, maxlen=maxlen)
    model.load_weights("weights/"+root_dir + "weights.h5")
    print("Веса:", model.weights[0])
    print("Количество объектов для предсказаний", len(X_recognize))
    arr = model.predict(X_recognize)
    arr1=[]
    for i in arr:
        arr1.append((i[0]))

    A = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    neuro_prediction = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
    for i in range(len(Z_recognize)):
        curr_len=Z_recognize[i]
        neuro_prediction[i]=[j for j in arr1[0:curr_len]]
        arr1= arr1[Z_recognize[i]:]



    return ([calculate_params(neuro_prediction,A,1),calculate_params(neuro_prediction,A,2),calculate_params(neuro_prediction,A,3)])


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
#print(Dict.convert_sentence("итак, будем веселиться, пока мы молоды! После веселой молодости, после горестной старости"))

#db=mysql_connect.connect()

def load_data_mixer(root_dir,section_dir,type_set):
    def read_data(root_dir,name,type_set):
        result=[]
        if type_set=="train":
            dir_open="result"
        else:
            dir_open="test_result"
        with open ("poem_base/"+root_dir+"/"+dir_open+"/"+name) as file:
            for i in file:
                result.append(int(i.replace("\n","")))
        return result
    if type_set=="train":
        dir1="poem_base/"+root_dir+"/result/"+section_dir[0]+"/"
        dir2="poem_base/"+root_dir+"/result/"+section_dir[1]+"/"
    else:
        dir1 = "poem_base/"+root_dir+"/test_result/"+section_dir[0]+"/"
        dir2 = "poem_base/"+root_dir+"/test_result/"+section_dir[1]+"/"
    num_files_1=(len(os.listdir(dir1))-1)
    num_files_2=(len(os.listdir(dir2))-1)
    type1_index=0
    type2_index=0
    result_X=[]
    result_Y=[]
    if type_set == "train":
        while (type1_index<num_files_1 or type2_index<num_files_2):
            if random.randint(0,1)==1:
                if type1_index<num_files_1:
                    result_X.append(read_data(root_dir,section_dir[0]+"/"+str(type1_index)+".txt",type_set))
                    result_Y.append([1])
                    type1_index+=1
                else:
                    result_X.append(read_data(root_dir,section_dir[1]+"/"+str(type2_index)+".txt",type_set))
                    result_Y.append([0])
                    type2_index+=1
            else:
                if type2_index<num_files_2:
                    result_X.append(read_data(root_dir,section_dir[1]+"/"+str(type2_index)+".txt",type_set))
                    result_Y.append([0])
                    type2_index += 1
                else:
                    result_X.append(read_data(root_dir,section_dir[0]+"/" + str(type1_index) + ".txt",type_set))
                    result_Y.append([1])
                    type1_index += 1
        #print(len(result_X))
        #print(np.array(result_Y))
    else:
        while type1_index<num_files_1:
            result_X.append(read_data(root_dir, section_dir[0] + "/" + str(type1_index) + ".txt", type_set))
            result_Y.append([1])
            type1_index += 1
        while type2_index<num_files_2:
            result_X.append(read_data(root_dir, section_dir[1] + "/" + str(type2_index) + ".txt", type_set))
            result_Y.append([0])
            type2_index += 1
    return [result_X,np.array(result_Y)]

def train(model,root_dir,section_dir):
    set_for_train = load_data_mixer(root_dir, section_dir, "train")
    set_for_test = load_data_mixer(root_dir, section_dir, "test")
    X_train = set_for_train[0]  # [[12,max_features-glush,14,111,14],[14,67,86,12],[134,64,86,32]]
    y_train = set_for_train[1]  # np.array([[0],[0],[0]])
    X_test = set_for_test[0]  # [[12,max_features-glush,15,111,14],[14,67,86,12],[134,64,86,32]]
    y_test = set_for_test[1]  # np.array([[0],[0],[0]])

    # Заполняем или обрезаем рецензии
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)

    # Обучаем модель
    history = model.fit(X_train, y_train, batch_size=64, epochs=5,
                        validation_data=(X_test, y_test), verbose=2)
    # Проверяем качество обучения на тестовых данных
    print("Обучение закончено")
    scores = model.evaluate(X_test, y_test,
                            batch_size=64)
    print(scores)
    return scores


def extract_train_from_file(file_name,max_features):
    lengts_poems=[]
    result_train=[]
    length_poem=0
    with open(file_name, "r") as file:
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

# Создаем сеть
model = Sequential()
# Слой для векторного представления слов
model.add(Embedding(max_features, 32))
model.add(SpatialDropout1D(0.2))
# Слой долго-краткосрочной памяти
model.add(LSTM(100, dropout=0.2, recurrent_dropout=0.2))
# Полносвязный слой
#model.add(Dense(glush, activation="sigmoid"))
model.add(Dense(1, activation="hard_sigmoid"))

# Копмилируем модель
model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])
print("Компиляция закончена")


def get_tags():
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

        self.setWindowTitle("Интерфейс нейронной сети")
        self.setFixedSize(600,900)  # запрещает изменять размер окна
        self.statusBar()
        self.setFont(QtGui.QFont("Times", 16, QtGui.QFont.Bold))
        self.adjustSize()

        self.tab1=QtGui.QTextEdit()
        self.tab2 = QtGui.QTextEdit()
        self.tab3= QtGui.QTextEdit()
        ##################################
        self.vBoxlayout1 = QtGui.QVBoxLayout()
        self.vBoxlayout2 = QtGui.QVBoxLayout()
        self.vBoxlayout3 = QtGui.QVBoxLayout()
        ##############
        self.label1 = QtGui.QLabel()
        self.label1.setFixedSize(550, 20)
        self.label1.setText("Введите текст стихотворения:")
        self.TextInput1 = QtGui.QTextEdit()
        self.TextInput1.setFixedSize(550, 600)

        self.PushButton1=QtGui.QPushButton()
        self.PushButton1.setFixedSize(550, 50)
        self.PushButton1.setText("Определить категории")

        self.TextOutput1 = QtGui.QTextEdit()
        self.TextOutput1.setFixedSize(550, 50)
        ##############

        self.label2 = QtGui.QLabel()
        self.label2.setFixedSize(550, 20)
        self.label2.setText("Выберите категорию для обучения:")
        self.combo2 = QtGui.QComboBox()
        self.combo2.setEditable(True)

        self.PushButton2 = QtGui.QPushButton()
        self.PushButton2.setFixedSize(550, 50)
        self.PushButton2.setText("Обучить")

        self.TextOutput2 = QtGui.QTextEdit()
        self.TextOutput2.setFixedSize(550, 500)

        self.PushButton21 = QtGui.QPushButton()
        self.PushButton21.setFixedSize(550, 50)
        self.PushButton21.setText("Сохранить веса")

        ##############
        self.label3 = QtGui.QLabel()
        self.label3.setFixedSize(550, 20)
        self.label3.setText("Выберите категорию с сохраненными весами:")
        self.combo3 = QtGui.QComboBox()
        self.combo3.setEditable(True)
        self.PushButton3 = QtGui.QPushButton()
        self.PushButton3.setFixedSize(550, 50)
        self.PushButton3.setText("Подобрать параметры")
        self.TextOutput3 = QtGui.QTextEdit()
        self.TextOutput3.setFixedSize(550, 500)

        ##############
        self.vBoxlayout1.addWidget(self.label1)
        self.vBoxlayout1.addWidget(self.TextInput1)
        self.vBoxlayout1.addWidget(self.PushButton1)
        self.vBoxlayout1.addWidget(self.TextOutput1)
        self.tab1.setLayout(self.vBoxlayout1)
        ##################################
        self.vBoxlayout2.addWidget(self.label2)
        self.vBoxlayout2.addWidget(self.combo2)
        self.vBoxlayout2.addWidget(self.PushButton2)
        self.vBoxlayout2.addWidget(self.TextOutput2)
        self.vBoxlayout2.addWidget(self.PushButton21)
        self.tab2.setLayout(self.vBoxlayout2)
        ##################################
        self.vBoxlayout3.addWidget(self.label3)
        self.vBoxlayout3.addWidget(self.combo3)
        self.vBoxlayout3.addWidget(self.PushButton3)
        self.vBoxlayout3.addWidget(self.TextOutput3)
        self.tab3.setLayout(self.vBoxlayout3)
        ##################################
        self.tab_widget = QtGui.QTabWidget()
        self.h_layout = QtGui.QWidget()

        self.tab_widget.addTab(self.tab1, 'Распознавание')
        self.tab_widget.addTab(self.tab2, 'Обучение')
        self.tab_widget.addTab(self.tab3, 'Подбор функции активации')
        self.hbox = QtGui.QHBoxLayout()
        self.hbox.addWidget(self.tab_widget)

        self.summary_box = QtGui.QVBoxLayout()  #
        self.summary_box.addLayout(self.hbox)
        self.h_layout.setLayout(self.summary_box)

        self.setCentralWidget(self.h_layout)
        menubar = self.menuBar()
        self.PushButton1.clicked.connect(self.on_click1)
        self.PushButton2.clicked.connect(self.on_click2)
        self.PushButton21.clicked.connect(self.on_click21)
        self.PushButton3.clicked.connect(self.on_click3)
        self.combo2.editTextChanged.connect(self.text_ch)
        self.tags=self.get_tags()
        self.tag_verbal_names=[x[0] for x in self.tags]
        self.root_dirs=[x[1] for x in self.tags]
        self.section_dirs=[[x[2],x[3]] for x in self.tags]
        self.add_names()

    def on_click1(self):
        input_poem=self.TextInput1.toPlainText()
        with open("new.txt","w")as file:
            file.write(input_poem)
        tags=get_tags()
        self.TextOutput1.setText(tags)

    def on_click2(self):
        self.index=self.combo2.currentIndex()
        self.TextOutput2.setText(str(self.index))
        self.root_dir=self.root_dirs[self.index]
        self.section_dir=self.section_dirs[self.index]
        self.tag_verbal_name=self.tag_verbal_names[self.index]
        result_train=train(model,self.root_dir,self.section_dir)
        output="Точность на тестовых даных\n %.2f%%" % (result_train[1]*100)
        self.TextOutput2.setText(str(output))

    def on_click21(self):
        model.save_weights("weights/"+self.root_dir+"weights.h5")
        self.TextOutput2.setText("Веса успешно сохранены")
        with open ("tags_added.txt","a+") as file:
            file.write("\n"+self.section_dir[0]+":"+self.tag_verbal_name)


    def on_click3(self):
        self.index = self.combo3.currentIndex()
        self.root_dir = self.root_dirs[self.index]
        self.section_dir = self.section_dirs[self.index]
        self.result_recognize = recognize(model, self.root_dir, self.section_dir)
        classic=(self.result_recognize[0])
        harrington=(self.result_recognize[1])
        double_waterfall=(self.result_recognize[2])
        str_TextOutput3="Минимальное число ошибок с использованием классической статистической модели\n"
        str_TextOutput3+=str(classic[0]) + " из 20"
        str_TextOutput3 += "\nМинимальное число ошибок с использованием модели Харрингтона\n"
        str_TextOutput3 += str(harrington[0])+ " из 20"
        str_TextOutput3 += "\nМинимальное число ошибок с использованием модели с 2-мя пороговыми функциями активации\n"
        str_TextOutput3 += str(double_waterfall[0])+ " из 20"

        result=[classic,harrington,double_waterfall]
        best_func=result.index(min(result))

        with open ("params/"+self.root_dir+"params.txt","w") as file:
            if best_func == 0:
                file.write("0:"+str(classic[1][0]))
            if best_func == 1:
                file.write("1:" + str(classic[1][0])+":"+str(classic[1][1])+":"+str(classic[1][2]))
            if best_func == 2:
                file.write("2:" + str(double_waterfall[1][0]) + ":" + str(double_waterfall[1][1]))
        self.TextOutput3.setText(str_TextOutput3)


    def get_tags(self):
        result=[]
        with open("tags.txt","r") as file:
            for str in file:
                tag_name=str.replace("\n","").split(":")
                result.append(tag_name)
        return result

    def add_names(self):
        for name in self.tag_verbal_names:
            self.combo2.addItem(name)
            self.combo3.addItem(name)

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


app = QtGui.QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())




