#!/usr/bin/python
# -*- coding: cp1251 -*-
#import mysql_connect
import re
import os
import numpy as np

import os
import random
from collections import deque
import matplotlib.pyplot as plt
import sys
from PyQt4 import QtGui, QtCore
import math

def gen_code(num_pages,border_what,border_attr,border_value,container_what,container_attr,container_value):
    pass

class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.setFixedSize(600,900)  # запрещает изменять размер окна
        self.statusBar()

        self.tab1=QtGui.QTextEdit()
        self.tab2 = QtGui.QTextEdit()
        self.tab3= QtGui.QTextEdit()
        ##################################
        self.vBoxlayout1 = QtGui.QVBoxLayout()
        self.vBoxlayout2 = QtGui.QVBoxLayout()
        self.vBoxlayout3 = QtGui.QVBoxLayout()
        ##############
        self.TextInput1Link = QtGui.QLineEdit()
        self.TextInput1Link.setFixedSize(550, 20)

        self.TextInput1Pages = QtGui.QLineEdit()
        self.TextInput1Pages.setFixedSize(550, 20)

        self.TextInput1Border = QtGui.QLineEdit()
        self.TextInput1Border.setFixedSize(550, 20)

        self.combo11Border = QtGui.QComboBox()
        self.combo11Border.setEditable(False)

        self.TextInput11Border = QtGui.QLineEdit()
        self.TextInput1Border.setFixedSize(550, 20)

        self.TextInput1Container = QtGui.QLineEdit()
        self.TextInput1Container.setFixedSize(550, 20)

        self.combo1Container=QtGui.QLineEdit()
        self.combo1Container.setFixedSize(550, 20)

        self.TextInput11Container=QtGui.QLineEdit()
        self.TextInput11Container.setFixedSize(550, 20)

        self.PushButton1 = QtGui.QPushButton()
        self.PushButton1.setFixedSize(550, 50)

        self.TextOutput = self.combo1Container=QtGui.QTextEdit()
        self.TextOutput.setFixedSize(550, 300)
        ##############

        self.combo2 = QtGui.QComboBox()
        self.combo2.setEditable(True)

        self.PushButton2 = QtGui.QPushButton()
        self.PushButton2.setFixedSize(550, 50)

        self.TextInput2 = QtGui.QLineEdit()
        self.TextInput2.setFixedSize(550,20)

        self.TextOutput2 = QtGui.QTextEdit()
        self.TextOutput2.setFixedSize(550, 500)

        self.PushButton21 = QtGui.QPushButton()
        self.PushButton21.setFixedSize(550, 50)

        ##############
        self.combo3 = QtGui.QComboBox()
        self.combo3.setEditable(True)
        self.PushButton3 = QtGui.QPushButton()
        self.PushButton3.setFixedSize(550, 50)
        self.TextOutput3 = QtGui.QTextEdit()
        self.TextOutput3.setFixedSize(550, 500)

        ##############
        self.vBoxlayout1.addWidget(self.TextInput1Pages)
        self.vBoxlayout1.addWidget(self.TextInput1Border)
        self.vBoxlayout1.addWidget(self.combo11Border)
        self.vBoxlayout1.addWidget(self.TextInput11Border)
        self.vBoxlayout1.addWidget(self.TextInput1Container)
        self.vBoxlayout1.addWidget(self.combo1Container)
        self.vBoxlayout1.addWidget(self.TextInput11Container)
        self.vBoxlayout1.addWidget(self.PushButton1)
        self.vBoxlayout1.addWidget(self.TextOutput)
        self.tab1.setLayout(self.vBoxlayout1)
        ##################################
        self.vBoxlayout2.addWidget(self.combo2)
        self.vBoxlayout2.addWidget(self.PushButton2)
        self.vBoxlayout2.addWidget(self.TextInput2)
        self.vBoxlayout2.addWidget(self.TextOutput2)
        self.vBoxlayout2.addWidget(self.PushButton21)
        self.tab2.setLayout(self.vBoxlayout2)
        ##################################
        self.vBoxlayout3.addWidget(self.combo3)
        self.vBoxlayout3.addWidget(self.PushButton3)
        self.vBoxlayout3.addWidget(self.TextOutput3)
        self.tab3.setLayout(self.vBoxlayout3)
        ##################################
        self.tab_widget = QtGui.QTabWidget()
        self.h_layout = QtGui.QWidget()

        self.tab_widget.addTab(self.tab1, 'Проверить сайт')
        self.tab_widget.addTab(self.tab2, 'Добавление категории')
        self.tab_widget.addTab(self.tab3, 'Загрузка стихотворений')
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
        num_pages=self.TextInput1Pages.toPlainText()
        border_what=self.TextInput1Border.toPlainText()
        border_attr=self.combo11Border.text()
        border_value=self.TextInput11Border.toPlainText()

        container_what=self.TextInput1Container.toPlainText()
        container_attr=self.combo1Container.text()
        container_value=self.TextInput1Container.toPlainText()
        gen_code(num_pages,border_what,border_attr,border_value,container_what,container_attr,container_value)


    def on_click2(self):
        self.index=self.combo2.currentIndex()
        self.TextOutput2.setText(str(self.index))
        self.root_dir=self.root_dirs[self.index]
        self.section_dir=self.section_dirs[self.index]
        result_train=train(model,self.root_dir,self.section_dir)
        self.TextOutput2.setText(str(result_train))

    def on_click21(self):
        model.save_weights("weights/"+self.root_dir+"weights.h5")
        self.TextOutput2.setText("Веса успешно сохранены")

    def on_click3(self):
        self.index = self.combo3.currentIndex()
        self.root_dir = self.root_dirs[self.index]
        self.section_dir = self.section_dirs[self.index]
        self.result_recognize = recognize(model, self.root_dir, self.section_dir)
        str_TextOutput3="Минимальное число ошибок с использованием классической статистической модели\n"
        str_TextOutput3+=str(self.result_recognize[0])
        str_TextOutput3 += "\nМинимальное число ошибок с использованием модели Харрингтона\n"
        str_TextOutput3 += str(self.result_recognize[1])
        str_TextOutput3 += "\nМинимальное число ошибок с использованием модели с 2-мя пороговыми функциями активации\n"
        str_TextOutput3 += str(self.result_recognize[2])

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

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())