import sys
import axi
import pdb
from xml.dom import minidom

import drawing_util, colors
from WaterpostOptions import DefaultOpts, SaveImageOpts


def draw_svg(svgFilename, opts=DefaultOpts):
    doc = minidom.parse(svgFilename)
    xmlPaths = doc.getElementsByTagName('path')
    paths = []
    for path in xmlPaths:
        curr = []
        pathData = path.attributes['d'].value
        moves = pathData.split('M')
        lines = []
        for move in moves:
            lines += move.split('L')
        for line in lines:
            if len(line) == 0:
                continue
            try:
                curr += [tuple(map(float, line.strip().split(' ')))]
            except Exception:
                pdb.set_trace()
        paths += [curr]
    drawing = axi.Drawing(paths).scale_to_fit(6.5, 4.5)
    drawing = drawing.center(7, 5)
    i = 0
    for path in drawing.paths:
      colors.color_brush(7)
      i += 1
      drawing_util.render_drawing(axi.Drawing([path]), opts=opts)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'usage: draw_svg_emoji '
        exit()
    emoji_code = sys.argv[1]

    draw_svg(emoji_code, opts=DefaultOpts)
