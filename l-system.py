# l-system.py

'''
axiom: F
rules: F -> C0FF-[C1-F+F+F]+[C2+F-F-F]
con F = forward
C0 = color tallo
- = rotate -radian(25)
+ = rotate +radian(25)
[ = save the state
] = load the state
'''
from turtle import *
from tkinter import *
import turtle

#Set up the screen
wn = turtle.Screen()
wn.bgcolor("white")
wn.tracer(3)

pivot = turtle.Turtle()
pivot.color("brown")
pivot.speed(0)
pivot.up()
pivot.setposition(0,-300)
pivot.down()
pivot.left(90)

leng = 150
penlen= 3
axiom = 'F'
s = ""
s += axiom
pivot.pensize(penlen)
stack = []
rules = {'F':"C0FF-[C1-F+F+F]+[C2+F-F-F]"}
stack = []

def generate():
    newString = ""
    global s

    #making the devivations
    
    for c in s:
       
        if c == 'F':
            newString += rules['F']
        else:
            newString += c
            
            
    s = newString

def write():
    global leng
    global s
    global penlen
    penlen *= .5
    leng *= .5

    #making the devivations
    
    for c in s:
       
        if c == 'F':
            pivot.forward(leng)
        elif c == '-':
            pivot.left(25)
        elif c == '+':
            pivot.right(25)
        elif c == '[':
            v1 = [pivot.xcor(),pivot.ycor(),pivot.heading()]
            stack.append(v1)
        elif c == ']':
            v1 = stack.pop()
            pivot.up()
            pivot.setposition(v1[0],v1[1])
            pivot.setheading(v1[2])
            pivot.down()
        elif c == '0':
            pivot.color("brown")
        elif c == '1':
            pivot.color("green")
        elif c == '2':
            pivot.color("green")


def resetPosition():
    pivot.setposition(0,-300)


for i in range(7):
    pivot.pensize(penlen)
    generate()
    resetPosition()
    write()
    print(s)
    print("\n")
