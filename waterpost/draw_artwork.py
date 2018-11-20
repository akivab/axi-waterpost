import pdb

import axi
import sys
import json
import colors
from drawing_util import render_drawing
from WaterpostOptions import WaterpostOptions, DefaultOpts, SaveImageOpts

FULL_PAPER_BOUNDS = (8, 8)
POSTCARD_BOUNDS = (6.5, 4.5)
POSTCARD_CENTER = (7, 5)
BOUNDS = POSTCARD_BOUNDS
CENTER = POSTCARD_CENTER
MIN_REBRUSH = 5 # 5 Inches per color

def draw_artwork(artworkData, opts=DefaultOpts):
    """

    :type artworkData: dict
    :type opts: WaterpostOptions
    """
    artwork = artworkData['artwork']
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
            last_color_tag = line[1]
            color_breaks[len(turtle.drawing.paths)] = (line[1], True)
        if arg == 'circle':
            opts.dbg('circle', line[1], line[2])
            turtle.circle(line[1], line[2], steps=90)
        if arg == 'forward':
            opts.dbg('forward', line[1])
            turtle.forward(line[1])
    drawing = turtle.drawing.scale_to_fit(*BOUNDS)
    drawing = drawing.center(*CENTER)

    # remove color breaks without color change that are for paths that are too small
    path_length_after_coloring = 0
    for path_idx in xrange(len(drawing.paths)):
        current_path_length = axi.path_length(drawing.paths[path_idx])
        if path_idx in color_breaks:
            if not color_breaks[path_idx][1] and path_length_after_coloring + current_path_length < MIN_REBRUSH:
                color_breaks.pop(path_idx, None)
                path_length_after_coloring += current_path_length
            else:
                path_length_after_coloring = current_path_length


    path_idx = 0
    current_paths = []
    last_brush_color = 0
    opts.useBrush = True
    while path_idx < len(drawing.paths):
        if path_idx in color_breaks:
            if len(current_paths):
                render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, opts=opts)
            current_paths = [drawing.paths[path_idx]]
            colors.color_brush(color_breaks[path_idx][0], lastColorTagName=last_brush_color, dipInWater=color_breaks[path_idx][1], opts=opts)
            last_brush_color = color_breaks[path_idx][0]
            turtle.penup()
        else:
            current_paths += [drawing.paths[path_idx]]
        path_idx += 1
    render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, opts=opts)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    data = json.loads(open(sys.argv[1], 'r').read())
    draw_artwork(data, opts=SaveImageOpts)
