#!/usr/bin/python
# -*- coding: cp1251 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
name_dir="revolution"
name_category="no_section"

url1='http://www.stihi.ru/2018/02/09/8797'
url2='http://www.stihi.ru/avtor/mborovkova'

#&s=50
#'http://www.stihi.ru/avtor/gomer3'
#html_doc = urlopen(url2).read()
#2018/02/11/10904
#http://www.stihi.ru/avtor/poeziya1
#http://www.stihi.ru/avtor/agata8

#author="none"

def read_author_links():
    result=[]
    html_doc_parent = urlopen('http://www.stihi.ru/authors')
    soup = BeautifulSoup(html_doc_parent, "html5lib")
    authors=soup.find_all('a',class_='recomlink')
    for i in authors:
        result.append(str(i.get('href')).replace('/avtor/',""))
    return result

#print(read_author_links())
print(os.getcwd())

def read_poem_links(link):

    global author
    a_all = []
    for i in range(1, 2):
        html_doc_parent = urlopen(
            link)#+'?page=' + str(i))  # =open("rev.html","r")
        # html_doc_parent=urlopen('http://stih.su/revolyuciya/')
        soup = BeautifulSoup(html_doc_parent, "html5lib")
        a2 = soup.find_all('h2', class_='node-title')
        a_page = []

        for a in a2:
            a_page.append(a.next.get('href'))
        a_all.append(a_page)
    return a_all

def create_poem_files(a_all,author_meta):
    try:
        os.makedirs("author/"+author_meta+"/"+name_category+"/texts")
        os.makedirs("author/" + author_meta + "/" + name_category + "/meta")
    except:
        pass
    try:
        os.makedirs("author/" + author_meta + "/test/" + name_category + "/texts")
        os.makedirs("author/" + author_meta + "/result/" + name_category)
        os.makedirs("author/" + author_meta + "/test_result/" + name_category)
    except:
        pass
    i=0
    for a2 in a_all:
        for a in a2:

                html_doc_poem=urlopen('https://stihi-russkih-poetov.ru'+str(a))

                soup = BeautifulSoup(html_doc_poem, "html5lib")
                title = (soup.find('h1', id='page-title'))
                author = (soup.find('div', class_='field-items').next.next)
                text = (soup.find('div',
                                  class_='field field-name-body field-type-text-with-summary field-label-hidden').next.next)
                text = str(text).replace('<div class="field-items">', '').replace('<div>', '').replace('<p>',
                                                                                                       '').replace(
                    '</p>', '').replace('<br/>', '').replace('</div>', '')
                #print(text)
                try:
                    with open('author/'+author_meta+'/'+name_category+'/texts/' + str(i) + '.txt', 'w',encoding='cp1251') as file:
                                file.write(text)
                        #print(str(title.next),str(author.next))
                    with open('author/'+author_meta+'/'+name_category+'/meta/' + str(i) + '.txt', 'w',encoding='cp1251') as file:
                                file.write("title:\n"+str(title.next)+"\nauthor:\n"+str(author.next))
                    i += 1
                except:
                    pass
            #except:
                #print("Russ              link!!!!!!")


def check_poem(a_all):
    html_doc_poem = urlopen('https://stihi-russkih-poetov.ru' + str(a_all[0][0]))
    soup = BeautifulSoup(html_doc_poem, "html5lib")
    title = (soup.find('h1', id='page-title'))
    author = (soup.find('div', class_='field-items').next.next)
    text = (soup.find('div',
                      class_='field field-name-body field-type-text-with-summary field-label-hidden').next.next)
    text = str(text).replace('<div class="field-items">', '').replace('<div>', '').replace('<p>',                                                                                 '').replace(
        '</p>', '').replace('<br/>', '').replace('</div>', '')
    return [text, author, title]


#print(soup)
#for i in read_author_links():
#    create_poem_files(read_poem_links(),i)

#create_poem_files(read_poem_links(),"no_section")