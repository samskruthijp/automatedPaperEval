import re


engweights=[1,2,3]
sciweights=[3,2,1]
socweights=[2,3,1]

finw=[]
subject=input("Enter the subject\n")
if subject=="english":
    schema = open('engschema.txt', 'r',encoding ="utf8").read()
    stuanswers = open('enganswers.txt', 'r',encoding ="utf8").read()
    finw=engweights
elif subject=="science":
    schema = open('scischemaup', 'r',encoding ="utf8").read()
    stuanswers = open('scianswersup', 'r',encoding ="utf8").read()
    finw=sciweights
elif subject=="social science":
    schema = open('socschema.txt', 'r',encoding ="utf8").read()
    stuanswers = open('socanswers.txt', 'r',encoding ="utf8").read()
    finw=socweights
else:
    print("subject not available")


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
print(number)
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
    
b=[]
b=re.split('end of solution',stuanswers)


print('ANSWER SHEET:\n\n')
stans=dict()
print("Question number array:")
snumber=[]
sanswer=[]
for  st in b:
    ele=re.split('question number',st)
    tkey=re.findall('[0-9]',ele[0])
    print(tkey)
    tfkey=''.join(tkey)
    stans[tfkey]=ele[1]

print(stans)
print(stans.keys())
print("\n\n")


totalmarks=0

from grammarbot import GrammarBotClient
from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
doc=[]

sum1=0
sum2=0
sum3=0
for i in range(len(number)):
    if number[i] in stans.keys():
        sanswer=stans[number[i]]
        
    else:
        continue
    #KEYWORDS
    doc=[answer[i],sanswer]
    sparse_matrix = count_vectorizer.fit_transform(doc)
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=['answer[i]','sanswer'])
    
    sim=(cosine_similarity(df, df))
    m=marks[i]*sim[0][1]
    sum1+=m
    print("Marks awarded for answer {}:".format(i+1))
    print("Based on keywords: {}".format(m))
   
    #MEANING
    Token_Set_Ratio = fuzz.token_set_ratio(answer[i],sanswer)
    print("Based on meaning: {}".format((Token_Set_Ratio/100)*marks[i]))
    sm=marks[i]*(Token_Set_Ratio/100)
    sum2=sum2+sm

    #GRAMMAR
    count=0
    newm=marks[i]
    
    client = GrammarBotClient()
    client = GrammarBotClient(api_key='KS9C5N3Y')
    text = sanswer
    res = client.check(text)
    match=res.matches
   
    for j in range(len(match)):
        
        match0=match[j]
        if (match0.category!= 'TYPOGRAPHY'):
            count+=1
    print("Number of gramatical mistakes: {}".format(count))
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
    print("Based on grammar: {}".format(newm))
    sum3=sum3+newm

    tm1=(Token_Set_Ratio* finw[1]+ (sim[0][1]*100*finw[0]) + ((newm/marks[i]))*100*finw[2])/6
    
    print("Percentage of total marks awarded: {}".format(tm1))
    print("Total marks: {}".format(round((tm1/100)*marks[i])))
    totalmarks=totalmarks+round((tm1/100)*marks[i])
    print("\n\n")
    
print("Marks obtained by similarity: {}".format(sum2))
print("Marks Obtained by keywords: {} ".format(sum1))
print("Marks Obtained by grammar: {}\n\n ".format(sum3))

print("Percentage based on keywords: {}%".format((sum1/sum(marks))*100))
print("Percentage based on similarity: {}%".format((sum2/sum(marks))*100))
print("Percentage based on grammar: {}%\n\n".format((sum3/sum(marks))*100))

print("Total marks: {} ".format(sum(marks)))
print("Total marks obtained by student: {}".format(round(totalmarks)))
print("Total percentage: {}%".format(round((totalmarks/sum(marks))*100)))




