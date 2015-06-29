#read text file========================================================
f = open("textfile.txt", "w+")
for i in range(10):
    f.write("This is line %d\n" % (i + 1))
f.close()

f = open("textfile.txt", "r")
if f.mode == 'r':  # check to make sure that the file was opened
    fl = f.readlines()  # reads the individual lines into a list
    for x in fl:
        print x

#buffer big file
buffersize = 50000
infile = open('bigfile.txt')
outfile = open('new.txt', 'w')

buffer = infile.read(buffersize)
while len(buffer):
    outfile.write(buffer)
    buffer = infile.read(buffersize)
print('done')

# os========================================================
# some shell support in shutil
from os import path
import os

# Check for item existence and type
print "Item exists: " + str(path.exists("textfile.txt"))
print "Item is a file: " + str(path.isfile("textfile.txt"))
print "Item is a directory: " + str(path.isdir("textfile.txt"))
  
# Work with file paths
print "Item's path: " + str(path.realpath("textfile.txt"))
print "Item's path and name: " + str(path.split(path.realpath("textfile.txt")))

# rename file, eliminate digital in file name
def rename_file():
    p = '/Users/ZhuJiaqi 1/Documents/Spyder_WorkSpace/Snippets/Python2/prank'
    file_list = os.listdir(p)
    print "Current dir: " + os.getcwd()
    os.chdir(p)

    for file_name in file_list:
        os.rename(file_name,file_name.translate(None,'0123456789'))

# can open web browser
import time
import webbrowser

time.sleep(5)
webbrowser.open('http://www.google.com')
