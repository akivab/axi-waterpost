import axi
import sys
import json

from write_message import get_message_height


def main(filename):
    data = json.loads(open(filename, 'r').read())
    signature = data['signature']
    turtle = axi.Turtle()
    for line in signature:
        arg = line[0]
        if arg == 'penup':
            print 'penup'
            turtle.penup()
        if arg == 'pendown':
            print 'pendown'
            turtle.pendown()
        if arg == 'move':
            print 'move', line[1:]
            turtle.goto(line[1], line[2])
        if arg == 'color':
            print 'changing color to ', line[1]
    drawing = turtle.drawing.rotate(-90)
    drawing = drawing.scale_to_fit(3, 1)
    height = get_message_height(filename)
    drawing = drawing.translate(0.5, height + 0.5)
    axi.draw(drawing)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    main(sys.argv[1])
