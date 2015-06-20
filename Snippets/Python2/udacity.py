# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:52:49 2015

@author: ZhuJiaqi
"""

import time
import webbrowser

time.sleep(5)
webbrowser.open('http://www.google.com')

#==============
import os

def rename_file():
    p = '/Users/ZhuJiaqi 1/Documents/Spyder_WorkSpace/Snippets/Python2/prank'
    file_list = os.listdir(p)
    print "Current dir: " + os.getcwd()
    os.chdir(p)

    for file_name in file_list:
        os.rename(file_name,file_name.translate(None,'0123456789'))
        

#==========
import turtle

def draw():
    window = turtle.Screen()
    window.bgcolor('green')
    
    brad = turtle.Turtle()
    brad.shape('turtle')
    brad.color('red')
    brad.speed(2)
    
    for i in range(4):
        brad.forward(100)
        brad.right(90)
    
    angie = turtle.Turtle()
    angie.shape('arrow')
    angie.color('blue')
    angie.circle(100)
    
    window.exitonclick()

def draw_square(brad):
    line_num = 0
    for i in range(4):
      brad.forward(150)
      brad.right(90)

def draw_art():
    window = turtle.Screen()
    window.bgcolor("red")
    brad = turtle.Turtle()
    brad.shape("circle")
    brad.color("white")
    brad.speed(100)
    square_num = 36
    brad = turtle.Turtle()
    for i in range (square_num):
       draw_square(brad)
       brad.right(10)
     
draw_art()

#===========================

# Download the twilio-python library from http://twilio.com/docs/libraries
from twilio.rest import TwilioRestClient
 
# Find these values at https://twilio.com/user/account
account_sid = "ACc19caa2b0daac4fd70aaf5f9f7278355"
auth_token = "510c29f9568ed25b1e21c91395152c76"
client = TwilioRestClient(account_sid, auth_token)
 
message = client.messages.create(to="+13522227518",from_="+15169861050",body="Hello there!")

















