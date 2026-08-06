'''
x = str(input("Enter a word: "))
x = x.replace(" ","")
mininum = min(x,key = x.count)
print("least frequent character are : ",mininum)
print("frequency is : ",x.count(mininum))
'''

'''
x = (input("Enter a string: "))
if not x.isalnum():
    print("It contains the special character")
else:
    print("No special character")  
    '''

t = [(12,35),(20,40),(30,60)]
digits=[int(d) for tup in t for num in tup for d in str(num)]
print("Digits: ",digits)  
freq={}
for item in digits:
    freq[item] = freq.get(item,0)+1
print("Frequencies: ",freq)    

from collections import defaultdict
words = ["eat","tea","ate","net","ten","own","now"]
anagrams = defaultdict(list)
for word in words:
    key = ' '.join(sorted(word))
    anagrams[key].append(word)
for group in anagrams.values():
    print(group)

    
s = input("enter a sentence: ")
w = s.split()
uw = list(dict.fromkeys(w))
ns = " ".join(uw)
print(ns)  

