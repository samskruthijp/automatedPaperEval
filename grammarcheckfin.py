#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import re
str = open('sampleschema.txt', 'r').read()

a=[]
a=re.split(',,...',str)
newl=[]
for st in a:
    ele=re.split('----|\t|-----',st)
    newl.append(ele)
   

number=[]
questions=[]
answer=[]
marks=[]
del(newl[-1])

for i in range(len(newl)):
        
        number.append(newl[i][0])
        questions.append(newl[i][1])
        answer.append(newl[i][2])
        marks.append(newl[i][3])
print('SCHEMA:\n\n')
print("Question number array:")
print(number)
print('\n\n')
print("Questions array:")
print(questions)
print('\n\n')
print("Answers array:")
print(answer)
print('\n\n')
marks=[int(x[1:]) for x in marks]
print('Marks array:')
print(marks)
print('\n\n')       
    
strup = open('sanswers.txt', 'r').read()
b=[]
b=re.split('-----',strup)


print('ANSWER SHEET:\n\n')
print("Question number array:")
snumber=[]
sanswer=[]
for  st in b:
    ele=re.split('----',st)
   
    snumber.append(ele[0])
    sanswer.append(ele[1])

print(snumber)
print('\n\n')
print("Answers array:")
print(sanswer)
print('\n\n')

from grammarbot import GrammarBotClient
for i in range(3):
    count=0
    client = GrammarBotClient()
    client = GrammarBotClient(api_key='KS9C5N3Y')
    #client = GrammarBotClient(base_uri='http://backup.grammarbot.io:80')
    text = sanswer[i]
    print(text)
    res = client.check(text)
    match=res.matches
   
    for j in range(len(match)):
        
        match0=match[j]
        if (match0.category!= 'TYPOGRAPHY'):
            count+=1
            """print(match0)
            print("Replacement offset:\n")
            print(match0.replacement_offset)
            print("Replacement length")
            print(match0.replacement_length)
            print("Suggestion way 1")
            print(match0.replacements)
            print("Suggestion way 2")
            print(match0.corrections)
            print("Suggestion way 3")
            print(match0.message)"""
    print(count)
    print(count/len(sanswer[i]))
    per=(count/len(sanswer[i]))*1000
    print((count/len(sanswer[i]))*1000)
    mard=int(per/10)
    print(mard)
    
