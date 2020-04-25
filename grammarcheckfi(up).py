import re



subject=input("Enter the subject\n")
if subject=="english":
    schema = open('engschema.txt', 'r',encoding ="utf8").read()
    stuanswers = open('enganswers.txt', 'r',encoding ="utf8").read()
    
elif subject=="science":
    schema = open('scischema.txt', 'r',encoding ="utf8").read()
    stuanswers = open('scianswers.txt', 'r',encoding ="utf8").read()
    
elif subject=="social science":
    schema = open('socschema.txt', 'r',encoding ="utf8").read()
    stuanswers = open('socanswers.txt', 'r',encoding ="utf8").read()
    
else:
    print("subject not available")



#str = open('scienceset.txt', 'r',encoding ="utf8").read()

a=[]
a=re.split(',,...',schema)
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
    
#strup = open('scienceans.txt', 'r',encoding ="utf8").read()
b=[]
b=re.split('-----',stuanswers)


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

totm=0
for i in range(len(sanswer)):
    count=0
    newm=marks[i]
    
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
    #SCIENCE 
    if(subject=="science"):
        if(marks[i]==3):
            if(count==3):
                newm=0.9*marks[i]
            elif(count>3):
                newm=0.9*marks[i]
                for k in range(4,count+1):
                    newm=0.98*newm
        elif(marks[i]==5):
            if(count==7):
                newm=0.9*marks[i]
            elif(count>7):
                newm=0.9*marks[i]
                for k in range(8,count+1):
                    newm=0.98*newm
        elif(marks[i]==7):
            if(count==10):
                newm=0.9*marks[i]
            elif(count>10):
                newm=0.9*marks[i]
                for k in range(11,count+1):
                  newm=0.98*newm  
                    
                    

    #SOCIAL
    elif(subject=="social science"):
        if(marks[i]==3):
            if(count==3):
                newm=0.9*marks[i]
            elif(count>3):
                newm=0.9*marks[i]
                for k in range(4,count+1):
                    newm=0.98*newm
        elif(marks[i]==5):
            if(count==7):
                newm=0.9*marks[i]
            elif(count>7):
                newm=0.9*marks[i]
                for k in range(8,count+1):
                    newm=0.98*newm
        elif(marks[i]==7):
            if(count==10):
                newm=0.9*marks[i]
            elif(count>10):
                newm=0.9*marks[i]
                for k in range(11,count+1):
                    newm=0.98*newm


    #ENGLISH
    elif(subject=="english"):
        if(marks[i]==8):
            if(count==6):
                newm=0.9*marks[i]
            elif(count>6):
                newm=0.9*marks[i]
                for k in range(7,count+1):
                    newm=0.98*newm

        elif(marks[i]==5):
            if(count==4):
                newm=0.9*marks[i]
            elif(count>4):
                newm=0.9*marks[i]
                for k in range(5,count+1):
                    newm=0.98*newm
        elif(marks[i]==4):
            if(count==3):
                newm=0.9*marks[i]
            elif(count>3):
                newm=0.9*marks[i]
                for k in range(4,count+1):
                    newm=0.98*newm
        elif(marks[i]==2):
            if(count==2):
                newm=0.9*marks[i]
            elif(count>2):
                newm=0.9*marks[i]
                for k in range(3,count+1):
                    newm=0.98*newm
    
    print(newm)
    totm=totm+newm
        
print("Marks by student",totm)
print("total marks",sum(marks))
            
    
'''print(count/len(sanswer[i]))
per=(count/len(sanswer[i]))*1000
print((count/len(sanswer[i]))*1000)
mard=int(per/10)
print(mard)'''

    
