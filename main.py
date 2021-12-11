from Hashing.ecdsa import *
import re
import string
import time

def checkStopword(sentence, stop_words):
    words = sentence.split(' ')
    result = [w for w in words if not w in stop_words]
    result = [w for w in result if len(w) > 1]
    sentence = ""
    for word in result:
        sentence = sentence + word + " "
    sentence = sentence.strip()
    return sentence

def stopwordRemove(textList):
    #stop_words = set(stopwords.words('english'))
    stop_words = ["a", "all", "an", "and", "any", "are", "as", "be", "been", "but", "by", "few", "for", "have", "he", "her", "here", "him", "his", "how", "i", "in", "is", "it", "its", "many", "me", "my", "none", "of", "on", "or", "our", "she", "some", "the", "their", "them", "there", "they", "that", "this", "us", "was", "what", "when", "where", "which", "who", "why", "will", "with", "you", "your"]
    text = []
    for i in range(len(textList)):
        text.append(checkStopword(textList[i], stop_words))
    return text

def biword_creation(textList):
    text = []
    for i in range(len(textList)):
        max = 0
        words = textList[i].split()
        freq = dict()
        res = ""
        for j in range(len(words)):
            words[j].lower()
            for k in range(len(words[j] ) - 1):
                word = words[j][k: k + 2]
                freq[word] = freq.get(word, 0) + 1
                if(max < freq[word]):
                    max = freq[word]
                    res = word
        if max == 1 and len(words) > 1:
            res = ""
        text.append(res)
    return text

def encrpytiontime_text():
    encryp_collection = []
    timetaken_enc = []
    for word in text:
        start_time = time.time()
        plain_text = word
        encrypted_text = C.ecc_encrypt(G, Pm, k, plain_text, UA[2])
        encryp_collection.append(encrypted_text)
        end_time = time.time()
        timetaken_enc.append(end_time - start_time)
    print(timetaken_enc)

def encrpytiontime_biword():
    encryp_collection_biword = []
    timetaken_biword_enc = []
    for word in biword:
        start_time = time.time()
        plain_text = word
        encrypted_text = C.ecc_encrypt(G, Pm, k, plain_text, UA[2])
        encryp_collection_biword.append(encrypted_text)
        end_time = time.time()
        timetaken_biword_enc.append(end_time - start_time)
    print(timetaken_enc)

def decryptiontime_text():
    timetaken_dec = []
    for enc_text in encryp_collection:
        start_time = time.time() 
        C.ecc_decrypt(enc_text, UB[1])
        end_time = time.time()
        timetaken_dec.append(end_time - start_time)
    print(timetaken_dec)

def decryptiontime_text():
    timetaken_biword_dec = []
    for enc_text in encryp_collection_biword:
        start_time = time.time() 
        C.ecc_decrypt(enc_text, UB[1])
        end_time = time.time()
        timetaken_biword_dec.append(end_time - start_time)
    print(timetaken_dec)

'''
For Printing Tables in Jupyter Notebook

For Encryption : 
    data = []
    data.append(["Text String","Text Encryption Time"])
    for i in range(len(text)):
        data.append([text[i],timetaken_enc[i]])

    display(HTML(
    '<table><tr>{}</tr></table><br><br>'.format(
    '</tr><tr>'.join(
        '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
    )
    ))

    data = []
    data.append(["Biword String","Biword Encryption Time"])
    for i in range(len(text)):
        data.append([biword[i],timetaken_biword_enc[i]])

    display(HTML(
    '<table><tr>{}</tr></table>'.format(
    '</tr><tr>'.join(
        '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
    )
    ))

For Decryption :
    data = []
    data.append(["Text String","Text Decryption Time"])
    for i in range(len(text)):
        data.append([text[i],timetaken_dec[i]])

    display(HTML(
    '<table><tr>{}</tr></table><br><br>'.format(
    '</tr><tr>'.join(
        '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
    )
    ))

    data = []
    data.append(["Biword String","Biword Decryption Time"])
    for i in range(len(text)):
        data.append([biword[i],timetaken_biword_dec[i]])

    display(HTML(
    '<table><tr>{}</tr></table>'.format(
    '</tr><tr>'.join(
        '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data)
    )
    ))
'''
