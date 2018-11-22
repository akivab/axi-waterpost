import axi
import sys
import json
from unidecode import unidecode

from drawing_util import render_drawing
from WaterpostOptions import WaterpostOptions, DefaultOpts


def write_message(artworkData, opts=DefaultOpts):
    """
    Renders a message
    :type artworkData: dict
    :type opts: WaterpostOptions
    """
    opts.dbg('writing message')
    drawing = get_message_drawing(artworkData)
    if drawing:
        render_drawing(drawing, opts=opts)


def get_message_drawing(artworkData, opts=DefaultOpts):
    """
    Returns a drawing of artwork data
    :type artworkData: dict
    :type opts: WaterpostOptions
    """
    message = unidecode(artworkData['message'])
    if len(message) == 0:
        return None
    opts.dbg('writing', message)
    font = axi.Font(axi.FUTURAL, 16)
    drawing = font.wrap(message, 3)
    drawing = drawing.translate(0.5, 0.5)
    drawing = drawing.remove_paths_outside(3.5, 3.5)
    return drawing


def get_message_height(artworkData):
    drawing = get_message_drawing(artworkData)
    if drawing:
        return drawing.height + 0.5
    return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    data = json.loads(open(sys.argv[1], 'r').read())
    write_message(data)
