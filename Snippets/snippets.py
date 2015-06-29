# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 23:18:02 2015

@author: ZhuJiaqi
"""
# loop=======================================================
days = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
for i, d in enumerate(days):
    print i, d

questions = ['name', 'quest', 'favorite color']
answers = ['lancelot', 'the holy grail', 'blue']
for q, a in zip(questions, answers):
    print 'What is your {0}? It is {1}.'.format(q, a)

knights = {'gallahad': 'the pure', 'robin': 'the brave'}
for k, v in knights.iteritems():
    print k, v

#data structure=====================================
#list
# append(x), extend(L), insert(i,x), remove(x), pop(), index(x)
#count(x), sort(), reverse(), deque(), popleft()
f = lambda x,y : x+y
reduce(f,range(10),0)

squares = [x**2 for x in range(10)]

#set
basket = ['apple', 'orange', 'apple', 'pear', 'orange', 'banana']
fruit = set(basket) # create a set without duplicates
'orange' in fruit # fast membership testing
'crabgrass' in fruit

a = set('abracadabra')
b = set('alacazam')
a - b # letters in a but not in b
a | b # letters in either a or b
a & b # letters in both a and b
a ^ b # letters in a or b but not both

a = {x for x in 'abracadabra' if x not in 'abc'}

#dictionary
d1 = {'one':1, 'two':2, 'three':3}
d2 = dict(a=1, b=2, c=3)
d3 = dict(name="dictionary", **d1)  #concat
d3

'one' in d1
d3.get('name')  #d3['name']

for k,v in d1.items():
    print(k,v)

#function===================================================
def fib(n):
    a,b = 0, 1
    while a < n:
        print a
        a, b = b , a+b

fib(1000)

#list and keywords args
def func(arg, *arguments, **keywords):
    print "arg: ", arg
    print "arguments: "
    for a in arguments:
        print a
    print "-" * 40
    keys = sorted(keywords.keys())
    for kw in keys:
        print kw, ":", keywords[kw]

func("humberger", "sorry", "really sorry",shopkeeper='Michael Palin', client="John Cleese",sketch="Cheese Shop Sketch")

tup = ("sorry1", "sorry2") #can also be list
kw = {'kw1' : "key1", 'kw2' : "key2"}
func("coffee", *tup, **kw)

#lambda functions
cube = lambda x: x ** 3
def fxy(f, x, y):   #use function as a argument
    return f(x) + f(y)

cube(3)
fxy(cube,2,3)

f = lambda x,y : x+y
reduce(f,range(10),0)


#generator
def isprime(n):
    if n == 1:
        return False
    for x in range(2, n):
        if n % x == 0:
            return False
    else:
        return True

def primes(n = 1):
   while(True):
       if isprime(n): yield n    #yield lazy generate
       n += 1 

for n in primes():      #use generator
    if n > 200: break
    print(n)

#regular expression
f = open('raven.txt')
for line in f:
    if re.search('(Len|Neverm)ore', line):
        print line

#sort comparator============================================
a = [[2, 3], [4, 6], [6, 1]]
a.sort(key=lambda x: x[1])
a

b = ['python', 'perl', 'java', 'c', 'haskell', 'ruby']
b.sort(key=lambda x: len(x))
b
#date========================================================
from datetime import date
from datetime import time
from datetime import datetime
from datetime import timedelta

today = date.today()
today
today.month
today.weekday()
now = datetime.now()

print now.strftime("%Y")
print now.strftime("%a, %d %B, %y")
print now.strftime("%c")
print now.strftime("%x")
print now.strftime("%X")
print now.strftime("%I:%M:%S %p") 
print now.strftime("%H:%M")

timedelta(weeks=2, days=3) + now
date(2015,12,25) - date.today()