# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 14:48:49 2019

@author: gu
"""
#For tika :- you need to be install java jdk above 7 version
#install and set enviourments varibles, then work on it

import tika
#tika.initVM()
from tika import parser
raw = parser.from_file('E:\\Data science\\proj\\resumes\\Adnan Alshater.pdf')
print(raw['content'])


        