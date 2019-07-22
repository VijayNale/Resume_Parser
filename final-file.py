# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 12:37:45 2019

@author: gu
"""
# =============================================================================
# Also create new enviourment varible in anacnoda : under that install pandas,numpy... , all packages
# first need to be install these package
# from anaconda navigator :- install nltk
# pip install tika
#first time run this code tika to download jar files from online added to Temp folder. wait to downlaod..............
# pip install docx2txt
# pip install spacy
# python -m spacy download en_core_web_sm
# 
# =============================================================================


import re,nltk,docx2txt,csv,os,datetime
import nltk
from nltk.corpus import stopwords
#run first time need to be download
#nltk.download('stopwords')   
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from tika import parser
#for tika you need to be install java jdk more than 7 and also set enviorment variable
#tika download jar files/install to java 


import spacy
from spacy.matcher import Matcher
# load pre-trained model
nlp = spacy.load('en_core_web_sm')
# initialize matcher with a vocab
matcher = Matcher(nlp.vocab)
###############################################################
def extract_name1(resume_text):
    nlp_text = nlp(resume_text)
    
    # First name and Last name are always Proper Nouns
    pattern = [{'POS': 'PROPN'}, {'POS': 'PROPN'}]
    
    matcher.add('NAME', None, pattern)
    
    matches = matcher(nlp_text)
    
    for match_id, start, end in matches:
        span = nlp_text[start:end]
        return span.text
#=================================================================

#============================================================
def extract_phone_numbers(string):
    #r = re.compile(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})')
    mobile = ""
    match_mobile = re.search(r'((?:\(?\+91\)?)?\d{10})',string)
    #phone_numbers = r.findall(string)
    #return [re.sub(r'\D', '', number) for number in phone_numbers]
    if(match_mobile != None):
        mobile = match_mobile.group(0)
    return mobile

#=============================================================
#this for multiple and rane from 8 to13
def extract_phone_numbers1(text):
    text= res
    phone = re.findall(r'[\+\(]?[1-9][0-9 .\-\(\)]{8,13}[0-9]', text)
    return phone
    
#==================================================================
            
#=============================================================
def extract_email_addresses(string):
    #string=fullText
    r = re.compile(r'[\w\.-]+@[\w\.-]+')
    return r.findall(string)
#==============================================================

#================================================================
def extract_names(document):
    #document = fullText
    nouns = [] #empty to array to hold all nouns
    stop = stopwords.words('english')
    stop.append("Resume")
    stop.append("RESUME")
    document = ' '.join([i for i in document.split() if i not in stop])
    sentences = nltk.sent_tokenize(document)
    for sentence in sentences:
        for word,pos in nltk.pos_tag(nltk.word_tokenize(str(sentences))):
            if (pos == 'NNP' and len(word)>2):
                nouns.append(word)
    nouns=' '.join(map(str,nouns))
    nouns=nouns.split()                
    return nouns            
#======================================================================

#======================================================
def modification_date(filename):
    import os.path, time
    return time.ctime(os.path.getmtime(path+filename))
#========================================================

#=======================================================
def generate_ngrams(filename, n):
    
    words = filename.split()
    output = []  
    for i in range(len(words)-n+1):
        output.append(words[i:i+n])
    f=[]            
    for i in output:
        if 'years' in i:
            f.append(output[output.index(i)])
            if len(f)==1:
                n=f[0][0]
                n=n + " " + "years"
                break
    
    if len(f)<1:
        n='Not specified'
    return n
#=============================================================================

def get_convert_to_text(filename):
    
    if filename.endswith(".docx"):
        fullText = docx2txt.process(path+filename)
        print(filename)
    elif filename.endswith(".doc"):
        parsed = parser.from_file(path+filename)
        fullText= parsed["content"]  #content of file
        print(filename)
    elif filename.endswith(".pdf"):
        raw = parser.from_file(path+file)
        print(filename)
        fullText=raw['content']
    else:
        print ("File format is currently not supported")
        exit(0)
    
    
    fullText= "for_name "+fullText
    fullText = re.sub("[^A-Za-z0-9.@\n " "]+"," ",fullText)
    details=[];ab=[];a=[]
    name_coll = extract_names(fullText)
    name_coll1 = extract_name1(fullText)
    fullText=fullText.replace('b"',"")
    stop = stopwords.words('english')
    stop.append("Resume")
    stop.append("RESUME")
    abc=fullText.split()
    
    b=extract_phone_numbers(fullText)
    c=set(extract_email_addresses(fullText))
    e=modification_date(filename)
    
    mi=fullText.lower()
    h=mi.replace("_"," ")
    h=h.replace("-"," ")
    h=h.replace(","," ")
    h=h.replace("("," ")
    h=h.replace(")"," ")
    h=h.replace(".docx"," ")
    h=h.replace(".pdf"," ")
    h=h.split()              #look at h only years get it
    if 'years' in h and 'months' in h:
        d=h[h.index('years')-1] + " " + h[h.index('years')]+ " " +h[h.index('months')-1] + " " +h[h.index('months')]
    elif 'months' in h:
        d=h[h.index('months')-1] + " " + h[h.index('months')]
    elif re.search('no experience',str(h),re.M|re.I) :
        d='No Experience'
    else:
        d=generate_ngrams(fullText, 2)  

    for i in name_coll :
        if re.search(i, str(c),re.M|re.I) or re.search(i,filename,re.M|re.I) :
            ab.append(i)
            if len(ab)==1:
                break
    
    #convert extracted into small letters
    fullText = fullText.lower()
    
    with open("E:\\Data science\\proj\\skill.txt","r") as skill:
        skill_set = skill.read().split("\n")            
    f=[]
    for s in skill_set:
        if s in fullText:
            if len(s)>2:
                f.append(s)                
        
    with open("E:\\Data science\\proj\\education.txt","r") as edu:
        edu_set = edu.read().split("\n")    
    educa=[]
    for s in edu_set:
        if s in fullText:
            if len(s)>2:
                educa.append(s)                
   
    #a='palak'
    a=abc[abc.index(ab[0])] + " " + abc[abc.index(ab[0])+1]      #its for matching
    c=" ".join(str(x) for x in c)
    details={'Name':a,'Name1':name_coll1,'Mob no':b,'Email':c,'Resume':filename,'Number of exp' : d,'Last Modified' : e,'Skills Set' : f,'Education': educa}
    return (details)

#==================================================================================================================
if __name__ == '__main__':
    output=[]
    #files_list=[]
    path = "E:\\Data science\\proj\\resumes\\"
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".docx"):
               output.append(get_convert_to_text(file))
            if file.endswith(".pdf"):
               output.append(get_convert_to_text(file))
            if file.endswith(".doc"):
                output.append(get_convert_to_text(file))

import pandas as pd
Data_frame = pd.DataFrame(output)
with open('E:\\Data science\\proj\Final_Data.csv', 'w') as csvfile:
    fieldnames = ['Name', 'Mob no','Email','Resume','Number of exp', 'Last Modified','Skills Set','Education']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(len(output)):
        writer.writerow(output[i])
print()
print("########Resume Filter############")
print("Please check the CSV file , Data loaded into it ")
    



#First to run all import package , funcition then main method