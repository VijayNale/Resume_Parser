# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 14:51:09 2019

@author: gu
"""       
from tika import parser
parsed = parser.from_file('E:\\Data science\\proj\\resumes\\\Resume.doc')
print(parsed["metadata"]) #To get the meta data of the file
print(parsed["content"]) # To get the content of the file
text= parsed["content"]



