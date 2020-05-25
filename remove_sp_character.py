from unidecode import unidecode

def result():
    file = open ("Extracted.txt", "a",encoding="utf-8")
    data = file.read()
    solution = _removeNonAscii(data)
    file.write(solution)
    file.close()

def _removeNonAscii(s): return "".join(i for i in s if ord(i)<128 and ord(i)>31)

    
    