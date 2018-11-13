# coding: utf-8
import axi
turtle = axi.Turtle()
print 'pen up'
turtle.penup()

print 'going to 8,3'
turtle.goto(8, 3)

print 'pen going down'
#turtle.pendown()
turtle.circle(1, 360)
turtle.penup()
turtle.goto(10, 3)
#turtle.pendown()
turtle.circle(1, 360)
turtle.penup()
turtle.goto(5,5)
#turtle.pendown()
for i in xrange(5): turtle.circle(i*5, 180)
drawing = turtle.drawing
axi.draw(drawing)
