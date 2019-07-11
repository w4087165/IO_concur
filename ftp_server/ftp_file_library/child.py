from time import sleep
import os
from multiprocessing import Process

def f1():
    for i in range(3):
        sleep(1)
        print('写代码')
def f2():
    for i in range(3):
        sleep(2)
        print('侧代码')
import math

f = ['Banana','Crange',"Apple","mango"]
f.insert(1,'K')
print(f)
sort_f = f[:-1]
sort_f.sort(key=lambda s:s[0])
print(sort_f)