import pdb

import axi
import sys
import json
import colors
from drawing_util import render_drawing
from WaterpostOptions import WaterpostOptions, DefaultOpts

FULL_PAPER_BOUNDS = (8, 8)
POSTCARD_BOUNDS = (5, 4)
POSTCARD_CENTER = (6.5, 5)
BOUNDS = POSTCARD_BOUNDS
CENTER = POSTCARD_CENTER


def draw_artwork(artworkData, opts=DefaultOpts):
    """

    :type artworkData: dict
    :type opts: WaterpostOptions
    """
    artwork = artworkData['artwork']
    rot = artworkData['artwork_rot'] if 'artwork_rot' in artworkData else 0
    turtle = axi.Turtle()
    color_breaks = {}
    last_color_tag = -1
    for line in artwork:
        arg = line[0]
        if arg == 'penup':
            opts.dbg('penup')
            turtle.penup()
        if arg == 'pendown':
            opts.dbg('pendown')
            turtle.pendown()
            curr_path = len(turtle.drawing.paths)
            if last_color_tag != -1 and curr_path not in color_breaks:
                color_breaks[curr_path] = (last_color_tag, False)
        if arg == 'move':
            opts.dbg('move', line[1:])
            turtle.goto(line[1], line[2])
        if arg == 'color':
            opts.dbg('changing color to ', line[1])
            color_breaks[len(turtle.drawing.paths)] = (line[1], True)
        if arg == 'circle':
            opts.dbg('circle', line[1], line[2])
            turtle.circle(line[1], line[2], steps=90)
        if arg == 'forward':
            opts.dbg('forward', line[1])
            turtle.forward(line[1])
    drawing = turtle.drawing.rotate(-90 * rot).scale_to_fit(*BOUNDS)
    drawing = drawing.center(*CENTER)

    path_idx = 0
    current_paths = []
    last_brush_color = 0
    while path_idx < len(drawing.paths):
        if path_idx in color_breaks:
            if len(current_paths):
                pdb.set_trace()
                surface = render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, opts=opts)
            current_paths = [drawing.paths[path_idx]]
            last_brush_color = color_breaks[path_idx][0]
            colors.color_brush(color_breaks[path_idx][0], color_breaks[path_idx][1], opts=opts)
            turtle.penup()
        else:
            current_paths += [drawing.paths[path_idx]]
        path_idx += 1
    return render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, opts=opts)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    data = json.loads(open(sys.argv[1], 'r').read())
    draw_artwork(data)
