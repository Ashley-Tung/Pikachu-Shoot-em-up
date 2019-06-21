def mode(numlist):
    return numlist[list(map(lambda x: numlist.count(x), numlist)).index(max(list(map(lambda x: numlist.count(x), numlist))))]

def fmode(functionList):
    return lambda x: mode(functionList[0](fmode(functionList[1:])(x)))

def enumerateTest(alist):
    for x,value in enumerate(alist,1):
        print(x, value)

def lengthOfLongestSubstring(s):
        lst = list()
        for c in s:
            lst.append(c)
            print(lst)
            print("end")
            if len(set(lst)) < len(lst):
                print("start if loop")
                print(set(lst))
                print(lst)
                lst.pop(0)
                print(lst)
                print("end if loop")
        return len(lst)

def count_palindromes(S):
    letters = set(S) #Give us a list of unique, individual letters in string
    words = 0 #counter for palindrome words
    for i in range(len(S)):
        for j in range(i+1, len(S)):
            if isPalindrome(S[i:j]):
                words = words+1
    count = len(letters)+words
    return count
    
    
def isPalindrome(S): #Checks if substring is paildrome
    i = 0
    j = len(S)-1
    while(i <= j):
        if S[i] != S[j]:
            return False
        i = i+1
        j = j-1
    return True

def fizzbuzz():
    for i in range(1,101):
        if i%3==0 and i%5==0:
            print('fizzbuzz')
        elif i%3==0:
            print("fizz")
        elif i%5 ==0:
            print("buzz")
        else:
            print(i)

def iBeforeEExceptAfterC(word):
    if "cie" in word:
        return False
    else:
        return True

def reverseString(s):
    if len(s) <=1:
        return s
    else:
        return s[len(s)-1]+reverseString(s[1:len(s)-1])+s[0]

letters = ["Z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y"]
def letterColumn(num):
    if num <=26:
        return letters[num%26]
    else:
        return letters[num%26]+letterColumn(num-26)



            

