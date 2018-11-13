import axi
import sys
import json
import colors

FULL_PAPER_BOUNDS = (8, 8)
POSTCARD_BOUNDS = (5, 4)
POSTCARD_CENTER = (6.5, 5)
BOUNDS = POSTCARD_BOUNDS
CENTER = POSTCARD_CENTER


def main(filename):
    data = json.loads(open(filename, 'r').read())
    artwork = data['artwork']
    rot = data['artwork_rot'] if 'artwork_rot' in data else 0
    turtle = axi.Turtle()
    color_breaks = {}
    last_color_tag = -1
    for line in artwork:
        arg = line[0]
        if arg == 'penup':
            print 'penup'
            turtle.penup()
        if arg == 'pendown':
            print 'pendown'
            turtle.pendown()
            curr_path = len(turtle.drawing.paths)
            if last_color_tag != -1 and curr_path not in color_breaks:
                color_breaks[curr_path] = (last_color_tag, False)
        if arg == 'move':
            print 'move', line[1:]
            turtle.goto(line[1], line[2])
        if arg == 'color':
            print 'changing color to ', line[1]
            color_breaks[len(turtle.drawing.paths)] = (line[1], True)
        if arg == 'circle':
            print 'circle', line[1], line[2]
            turtle.circle(line[1], line[2], steps=90)
        if arg == 'forward':
            print 'forward', line[1]
            turtle.forward(line[1])
    drawing = turtle.drawing.rotate(-90 * rot).scale_to_fit(*BOUNDS)
    drawing = drawing.center(*CENTER)

    path_idx = 0
    current_paths = []
    last_brush_color = 0
    colors.should_color_brush = False
    surface = None
    while path_idx < len(drawing.paths):
        if path_idx in color_breaks:
            if len(current_paths):
                surface = render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, surface=surface)
            current_paths = [drawing.paths[path_idx]]
            last_brush_color = color_breaks[path_idx][0]
            colors.color_brush(color_breaks[path_idx][0], color_breaks[path_idx][1])
            turtle.penup()
        else:
            current_paths += [drawing.paths[path_idx]]
        path_idx += 1
    render_drawing(axi.Drawing(current_paths), colorTag=last_brush_color, renderToFile=True, surface=surface)


def render_drawing(drawing, colorTag=0, renderToFile=False, surface=None):
    surface = drawing.render(bounds=(0,0,7,5), rgb=colors.COLOR_RGB[colorTag], surface=surface)
    if renderToFile:
        surface.write_to_png("output/image.png")
    # axi.draw(drawing)
    return surface


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    main(sys.argv[1])
