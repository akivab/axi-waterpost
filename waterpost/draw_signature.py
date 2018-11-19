import axi
import sys
import json

from WaterpostOptions import DefaultOpts
from write_message import get_message_height
from drawing_util import render_drawing


def draw_signature(artworkData, opts=DefaultOpts):
    signature = artworkData['signature']
    turtle = axi.Turtle()
    for line in signature:
        arg = line[0]
        if arg == 'penup':
            opts.dbg('penup')
            turtle.penup()
        if arg == 'pendown':
            opts.dbg('pendown')
            turtle.pendown()
        if arg == 'move':
            opts.dbg('move', line[1:])
            turtle.goto(line[1], line[2])
        if arg == 'color':
            opts.dbg('changing color to ', line[1])
    drawing = turtle.drawing.scale_to_fit(2.5, 0.8)
    height = get_message_height(artworkData)
    drawing = drawing.translate(1.0, height + 0.5)
    render_drawing(drawing, opts=opts)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    data = json.loads(open(sys.argv[1], 'r').read())
    draw_signature(data)
