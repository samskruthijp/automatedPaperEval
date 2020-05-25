import json

f = open('C:/Users/Shivani T Eswara/finyear/visionapi/uploaded files/pdf_result output-1-to-2.json', "w",encoding="utf-8")

data = json.load(f)

print(data)