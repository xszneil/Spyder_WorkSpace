# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 18:52:49 2015

@author: ZhuJiaqi
"""
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







