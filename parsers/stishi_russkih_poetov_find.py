#!/usr/bin/python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os

index=0

def find_authors_by_letter():

    try:
        os.makedirs("stihi_russkih_poetov/texts")
        os.makedirs("stihi_russkih_poetov/meta")
    except:
        pass
    html_doc_parent = urlopen('https://stihi-russkih-poetov.ru/authors-glossary/%D0%BF')
    soup = BeautifulSoup(html_doc_parent, "html5lib")
    row_authors=soup.find_all('span',class_="views-summary views-summary-unformatted")
    authors_starts_with_letter=[]
    for i in row_authors:
        authors_starts_with_letter.append(i.find('a').get('href'))
    #print (authors_starts_with_letter)
    return authors_starts_with_letter
def find_list_of_authors(arr):
    base_link='https://stihi-russkih-poetov.ru'
    for i in arr:
        html_doc=urlopen(base_link+i)
        soup = BeautifulSoup(html_doc, "html5lib")
        authors_list_row=soup.find_all('strong',class_='views-field views-field-name poem-author')
        for author in authors_list_row:
            link=author.find('a')
            author=link.next
            link_href=link.get('href')
            #print(author,link_href)
            find_poems_on_author(author,link_href)

def find_poems_on_author(author,link):
    base_link = 'https://stihi-russkih-poetov.ru'
    html_doc = urlopen(base_link + link)
    soup = BeautifulSoup(html_doc, "html5lib")
    poems_row=soup.find_all('h2',class_='node-title')
    poems=[]
    for i in poems_row:
        link_row=i.find('a')
        title=link_row.next
        link=link_row.get('href')
        #print(title,author,link)
        single_poem(title,author,link)

def single_poem(title,author,link):
    global index
    base_link = 'https://stihi-russkih-poetov.ru'
    html_doc = urlopen(base_link + link)
    soup = BeautifulSoup(html_doc, "html5lib")
    text_row=soup.find('div',class_='field field-name-body field-type-text-with-summary field-label-hidden')
    year=text_row.find('div',class_='field-items').next.next
    text=str(text_row.find('div',class_='field-items').next.next).replace('<p>','').replace('</p>','').replace('<br/>','')
    tags_row=soup.find('div',class_='field field-name-field-tags field-type-taxonomy-term-reference field-label-inline clearfix').find_all('a')
    tags=""
    for i in tags_row:
        tags+=str(i.next)+","
    #print (title,author,text)
    #print('tags!!!!!!!!!!!!!!!!!!!!!!!',tags)

    try:
        with open ('stihi_russkih_poetov/texts/'+str(index)+'.txt','w')as file:
            file.write(text)
        with open('stihi_russkih_poetov/meta/'+str(index)+'.txt', 'a')as file:
            file.write("author:\n"+author)
            file.write("\ntitle\n" + title)
            file.write("\ntags\n" + tags)
        index+=1
    except:
        print("Шальная кодировка")


#find_list_of_authors(find_authors_by_letter())