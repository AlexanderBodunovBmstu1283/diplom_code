import os
import re

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
sum=0
arr=[]

def extract_train_from_file(mode,dir_first,dir_second,max_features):
    lengts_poems=[]
    result_train=[]
    dir1="poem_base/"+dir_first+"/"+mode+dir_second+"/texts/"
    if mode=="test/":
       num_files_1 = (len(os.listdir(dir1)))
       print(num_files_1)
       file_current=1
    else:
        num_files_1 = (len(os.listdir(dir1)))-1
        print(num_files_1)
        file_current = 0
    while file_current <=num_files_1:
        length_poem=0
        with open("poem_base/"+dir_first+"/"+mode+dir_second+"/texts/" + str(file_current) + ".txt", "r",encoding="utf-8") as file:
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
        file_current+=1
        if mode=="test/":
            with open("poem_base/"+dir_first+"/length_poems.txt","a+") as file:
                file.write(str(length_poem)+",")
        else:
            with open("poem_base/"+dir_first+"/tag_length_poems.txt","a+") as file:
                file.write(str(length_poem)+",")

    print(result_train)
    return result_train

def write_result_to_files(mode_write,mode,dir_first,dir_second,max_features):
    vector_result=extract_train_from_file(mode,dir_first,dir_second,max_features)
    for i in range(len(vector_result)):
        with open ("poem_base/"+dir_first+"/"+mode_write+dir_second+"/"+str(i)+".txt","w") as file:
            for j in vector_result[i]:
                file.write(str(j)+"\n")
