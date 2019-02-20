#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
import shutil
name_dir="revolution"
name_category="marina_zvetaeva"

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

def decode_str(str):
    result_=""
    for word in str.split(" "):
        try:
            result_+=" "+word.encode("cp1252").decode("cp1251")
        except:
            pass
    return result_


def read_poem_links(link):

    global author
    a_all = []
    for i in range(1, 3):
        try:
            html_doc_parent = urlopen(
                link+'page/'+str(i)+'/')  # =open("rev.html","r")
            # html_doc_parent=urlopen('http://stih.su/revolyuciya/')
            soup = BeautifulSoup(html_doc_parent, "html5lib",from_encoding="utf8")
            a2 = soup.find_all('li', class_='title')
            a3=[]
            for i in a2:
                a3.append(i.find('a'))
            a_page = []

            for a in a3:
                a_page.append([a.get('href'),a.next])
            a_all.append(a_page)
            print(a_page[0])
        except:
            pass
    return a_all

def create_poem_files(a_all,author_meta,mode):
    try:
        os.makedirs(mode+author_meta+"/"+author_meta+"/texts")
        #os.makedirs(mode + author_meta + "/no_section/texts")

        os.makedirs(mode + author_meta + "/" + author_meta + "/meta")
        os.makedirs(mode + author_meta + "/" + author_meta + "/critics")
    except:
        pass
    try:
        os.makedirs(mode + author_meta + "/test/" + author_meta + "/texts")
        #os.makedirs(mode + author_meta + "/test/no_section/texts")
        os.makedirs(mode + author_meta + "/result/" + author_meta)
        #os.makedirs(mode + author_meta + "/result/no_section")
        os.makedirs(mode + author_meta + "/test_result/" + author_meta)
        #os.makedirs(mode + author_meta + "/test_result/no_section")
    except:
        pass
    if mode == "poem_base/":
        shutil.copytree("poem_base/to_child/no_section/", mode + author_meta + "/no_section/")
        shutil.copytree("poem_base/to_child/test/no_section/", mode + author_meta + "/test/no_section/")
        shutil.copytree("poem_base/to_child/result/no_section/", mode + author_meta + "/result/no_section/")
        shutil.copytree("poem_base/to_child/test_result/no_section/", mode + author_meta + "/test_result/no_section/")
    i=1
    count_all = len(a_all) * len(a_all[0])
    count_page = len(a_all[0])
    count_page_old = count_page
    for a2 in a_all:
        print(str(count_page / count_all * 100) + '%')
        count_page += count_page_old
        for a in a2:
                print(a[0])

                html_doc_poem=urlopen(str(a[0]))

                soup = BeautifulSoup(html_doc_poem, "html5lib",from_encoding="utf8")
                #title = str(soup.find('span', property='name').next).split(' - ')
                #author = title[0]
                #title=title[0]
                meta=a[1].split(" —")
                try:
                    author=meta[0]
                except:
                    author=""
                try:
                    title=meta[1]
                except:
                    title=""
                text = (soup.find('div',
                                  class_='poem-text').get_text())
                text = str(text).replace('<div class="field-items">', '').replace('<div>', '').replace('<p>',
                                                                                                       '').replace(
                    '</p>', '').replace('<br/>', '').replace('</div>', '')
                text=text.replace(#replace(".analiz { width: 234px; height: 60px; }@media(min-width: 320px) { .analiz { width: 300px; height: 250px; } }@media(min-width: 365px) { .analiz { width: 336px; height: 280px; } }@media(min-width: 728px) { .analiz { width: 728px; height: 90px; } }(adsbygoogle = window.adsbygoogle","")
                '''.analiz { width: 234px; height: 60px; }
@media(min-width: 320px) { .analiz { width: 300px; height: 250px; } }
@media(min-width: 365px) { .analiz { width: 336px; height: 280px; } }
@media(min-width: 728px) { .analiz { width: 728px; height: 90px; } }

(adsbygoogle = window.adsbygoogle''','')

                #title=decode_str(title)
                #author = decode_str(author)
                if '||' in text:
                    text=text.split("||")
                    poem_text=text[0]
                    poem_critics=text[1]
                else:
                    poem_text=text
                    poem_critics=""
                #print(text)
                print(poem_text)

                if i<11:
                    with open(mode + author_meta + '/test/' + author_meta + '/texts/' + str(i) + '.txt', 'w',
                              encoding="utf8") as file:
                        file.write(poem_text)
                else:
                    with open(mode+author_meta+'/'+author_meta+'/texts/' + str(i-11) + '.txt', 'w',encoding="utf8") as file:
                                    file.write(poem_text)
                    with open(mode + author_meta + '/' + author_meta + '/critics/' + str(i-11) + '.txt','w',encoding="utf8") as file:
                                    file.write(poem_critics)
                            #print(str(title.next),str(author.next))

                    with open(mode+author_meta+'/'+author_meta+'/meta/' + str(i-11) + '.txt', 'w',encoding="utf8") as file:
                                    file.write("title:\n"+str(title)+"\nauthor:\n"+str(author))
                i += 1
    return [poem_text, author, title,i]

def check_poem(a_all):
    html_doc_poem = urlopen(str(a_all[0][0][0]))
    soup = BeautifulSoup(html_doc_poem, "html5lib", from_encoding="utf8")
    meta=str(a_all[0][0][1]).split(" —")
    print(meta)
    author=meta[0]
    title=meta[1]
    text = (soup.find('div',
                      class_='poem-text').get_text())
    text = str(text).replace('<div class="field-items">', '').replace('<div>', '').replace('<p>',
                                                                                           '').replace(
        '</p>', '').replace('<br/>', '').replace('</div>', '')
    text = text.replace(
        # replace(".analiz { width: 234px; height: 60px; }@media(min-width: 320px) { .analiz { width: 300px; height: 250px; } }@media(min-width: 365px) { .analiz { width: 336px; height: 280px; } }@media(min-width: 728px) { .analiz { width: 728px; height: 90px; } }(adsbygoogle = window.adsbygoogle","")
        '''.analiz { width: 234px; height: 60px; }
@media(min-width: 320px) { .analiz { width: 300px; height: 250px; } }
@media(min-width: 365px) { .analiz { width: 336px; height: 280px; } }
@media(min-width: 728px) { .analiz { width: 728px; height: 90px; } }

(adsbygoogle = window.adsbygoogle''', '')

    #title = decode_str(title)
    #author = decode_str(author)
    if '||' in text:
        text = text.split("||")
        poem_text = text[0]
        poem_critics = text[1]
    else:
        poem_text = text
        poem_critics = ""
    # print(text)
    print(poem_text)
    return [poem_text, author, title]
    #except:
                #print("Russ              link!!!!!!")



#print(soup)
#for i in read_author_links():
#    create_poem_files(read_poem_links(),i)

#create_poem_files(read_poem_links(),"marina_zvetaeva")