import re
import os, io
from google.cloud import vision
from google.cloud import storage
from google.protobuf import json_format

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'ServiceAccountToken.json'

def upload_file(bucket_name, source_file_name, destination_blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )

def detect_document(gcs_source_uri, gcs_destination_uri, subject, filename):
    mime_type = 'application/pdf'
    batch_size = 2

    client = vision.ImageAnnotatorClient()

    feature = vision.types.Feature(
        type=vision.enums.Feature.Type.DOCUMENT_TEXT_DETECTION)
    
    gcs_source = vision.types.GcsSource(uri=gcs_source_uri)
    input_config = vision.types.InputConfig(
        gcs_source=gcs_source, mime_type=mime_type)

    gcs_destination = vision.types.GcsDestination(uri=gcs_destination_uri)
    output_config = vision.types.OutputConfig(
        gcs_destination=gcs_destination, batch_size=batch_size)

    async_request = vision.types.AsyncAnnotateFileRequest(
        features=[feature], input_config=input_config,
        output_config=output_config)

    operation = client.async_batch_annotate_files(
        requests=[async_request])

    print('Waiting for the operation to finish.')
    operation.result(timeout=180)

    storage_client = storage.Client()

    match = re.match(r'gs://([^/]+)/(.+)', gcs_destination_uri)
    bucket_name = match.group(1)
    prefix = match.group(2)
    print("bucket name is "+bucket_name)
    print("prefix is "+prefix)
    bucket = storage_client.get_bucket(bucket_name)

    # List objects with the given prefix.
    blob_list = list(bucket.list_blobs(prefix=prefix))
    print(blob_list)
    print('Output files:')
    for blob in blob_list:
        print(blob.name)
    
    fname = filename+'_solution.txt'
    answer_file = open (fname, "a",encoding="utf-8")

    for i in range(0, len(blob_list)):
        output = blob_list[i]

        json_string = output.download_as_string()
        response = json_format.Parse(
            json_string, vision.types.AnnotateFileResponse())


        for j in range(0, len(response.responses)):

            page_response = response.responses[j]
            annotation = page_response.full_text_annotation
            answer_file.write(annotation.text)
        
    answer_file.close()
    print("finished writing to file")

    #evaluate_answer(subject, filename, schema_path)


#upload_file('paperevaluation', 'C:/Users/Shivani T Eswara/finyear/visionapi/uploaded files/english.pdf', 'english_solution_gcp.pdf')
#detect_document('gs://paperevaluation/english_solution_gcp.pdf', 'gs://paperevaluation/english_result ')

def receive_file(subject, schema_path, answer_path):
    filename = (os.path.splitext(os.path.basename(answer_path))[0])
    destination_blob_name = filename+'_solution_gcp.pdf'
    upload_file('paperevaluation',answer_path,destination_blob_name)
    gcs_source_uri = 'gs://paperevaluation/'+destination_blob_name
    gcs_destination_uri = 'gs://paperevaluation/'+filename+'_result '
    detect_document(gcs_source_uri, gcs_destination_uri, filename)
    if subject=="english":
        fname='english1solution.txt'
        evaluate_answer(subject,fname,schema_path)
    elif subject="science":
        fname='scianswers.txt'
        evaluate_answer(subject,fname,schema_path)
    else:
        fname='social1solution1.txt'
        evaluate_answer(subject,fname,schema_path) 

def evaluate_answer(subject, answer_file, schema_path):
    import re
    fin=[]

    engweights=[1,2,3]
    sciweights=[3,2,1]
    socweights=[2,3,1]

    finw=[]
   
    if subject=="english":
        schema = open(schema_path, 'r',encoding ="utf8").read()
        stuanswers = open(answer_file, 'r',encoding ="utf8").read()
        finw=engweights
    elif subject=="science":
        schema = open(schema_path, 'r',encoding ="utf8").read()
        stuanswers = open(answer_file, 'r',encoding ="utf8").read()
        finw=sciweights
    elif subject=="social science":
        schema = open(schema_path, 'r',encoding ="utf8").read()
        stuanswers = open(answer_file, 'r',encoding ="utf8").read()
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

    for  st in b:
        
        ele=re.split('Question Number',st)
        #print(ele)
        tkey=re.findall('[0-9]',ele[0])
        #print(tkey)
        tfkey=''.join(tkey)
        stans[tfkey]=ele[1]

    for k,v in stans.items():
        print (k,v)
        print('\n')
        


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
        temp=[]
        if number[i] in stans.keys():
            sanswer=stans[number[i]]
            
        else:
            continue
        #KEYWORDS
        
        s1='Marks awarded to answer '+str(i+1)
        temp.append(s1)
        s1=''
        doc=[answer[i],sanswer]
        sparse_matrix = count_vectorizer.fit_transform(doc)
        doc_term_matrix = sparse_matrix.todense()
        df = pd.DataFrame(doc_term_matrix, 
                    columns=count_vectorizer.get_feature_names(), 
                    index=['answer[i]','sanswer'])
        
        sim=(cosine_similarity(df, df))
        m=marks[i]*sim[0][1]
        sum1+=m
        
        s2='Based on keywords: '+ str(m)
        temp.append(s2)
        s2=''
        #MEANING
        Token_Set_Ratio = fuzz.token_set_ratio(answer[i],sanswer)
        '''print("Based on meaning: {}".format((Token_Set_Ratio/100)*marks[i]))'''
        sm=marks[i]*(Token_Set_Ratio/100)
        s3='Based on meaning: '+ str(sm)
        sum2=sum2+sm
        temp.append(s3)
        s3=''
        

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
        #print("Number of gramatical mistakes: {}".format(count))
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
        '''print("Based on grammar: {}".format(newm))'''
        sum3=sum3+newm
        s4='Based on Grammar: '+ str(newm)
        temp.append(s4)
        s4=''
        
        tm1=(Token_Set_Ratio* finw[1]+ (sim[0][1]*100*finw[0]) + ((newm/marks[i]))*100*finw[2])/6
        
        #print("Percentage of total marks awarded: {}".format(tm1))
        '''print("Total marks: {}".format(round((tm1/100)*marks[i])))'''
        tmtm=round((tm1/100)*marks[i])
        s5='Total: ' + str(tmtm)
        temp.append(s5)
        s5=''
        totalmarks=totalmarks+round((tm1/100)*marks[i])
        fin.append(temp)
        print("\n\n")
    temp=[]
    s1='Total marks: ' +str((sum(marks)))
    temp.append(s1)
    s2='Total marks obtained by student: '+ str((round(totalmarks)))
    temp.append(s2)
    per=round((totalmarks/sum(marks))*100)
    s3='Percentage: '+ str(per)
    temp.append(s3)
    fin.append(temp)
   

    return fin



# if __name__=="__main__":
#     fin=[]
#     subject=input("Enter the subject\n")
#     fin=testing(subject)
#     print(fin)

#     for ele in fin:
#         for i in ele:
#             print(i)
#         print('\n')
    






    





