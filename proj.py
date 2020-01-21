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


from fuzzywuzzy import fuzz
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
count_vectorizer = CountVectorizer(stop_words='english')
count_vectorizer = CountVectorizer()
doc=[]
sum1=0
sum2=0
for i in range(len(answer)):
    doc=[answer[i],sanswer[i]]
    sparse_matrix = count_vectorizer.fit_transform(doc)
    doc_term_matrix = sparse_matrix.todense()
    df = pd.DataFrame(doc_term_matrix, 
                  columns=count_vectorizer.get_feature_names(), 
                  index=['answer[i]','sanswer[i]'])
    print("Similarity of answer {} with the Schema based on keywords:".format(i+1))
    sim=(cosine_similarity(df, df))
    print(sim[0][1])
    m=marks[i]*sim[0][1]
    sum1+=round(m)
    print("Marks awarded for answer {}:".format(i+1))
    print(m)
    print("Marks rounded to{}".format(round(m)))
   
    print("Similarity:")
    Token_Set_Ratio = fuzz.token_set_ratio(answer[i],sanswer[i])
    print(Token_Set_Ratio)
    print("similarity score: {}".format((Token_Set_Ratio/100)*marks[i]))
    sm=marks[i]*(Token_Set_Ratio/100)
    print("rounded to {}".format(round(sm)))
    sum2=sum2+round(sm)
    print("\n")
    
print("Marks obtained by similarity: {}".format(sum2))
print("Marks Obtained by keywords: {} ".format(sum1))
print("Total marks: {} ".format(sum(marks)))
print("Percentage based on keywords: {}%".format((sum1/sum(marks))*100))
print("Percentage based on similarity: {}%".format((sum2/sum(marks))*100))





    
    
           
