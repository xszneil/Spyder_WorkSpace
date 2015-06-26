'''
Created on 2014-7-15

@author: ZhuJiaqi
'''
#Implement a program directtree.py that takes a directectory as argument and prints all the files in that directectory recursively as a tree.
#Write a program to print directectory tree. The program should take path of a directectory as argument and print all the files in it recursively as a tree.

import os
direct='/Users/ZhuJiaqi/Desktop'
print direct
a='|--'
b='|   '
i=0
def directtree(direct,i):
    filenames=os.listdir(direct)
    for filename in filenames:
        if not os.path.isdir(os.path.abspath(direct+'/'+filename)):
            if filename==filenames[-1]:    
                print b*i+'\--',filename
            else:
                print b*i+'|--',filename
        else:
            print b*i+'|--',filename
            direct=direct+'/'+filename
            directtree(direct,i+1)

directtree(direct,i)