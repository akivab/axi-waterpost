import axi
import sys
import json
from unidecode import unidecode

from WaterpostOptions import DefaultOpts, WaterpostOptions
from drawing_util import render_drawing


def write_address(artworkData, opts=DefaultOpts):
    """

    :type artworkData: dict
    :type opts: WaterpostOptions
    """
    opts.dbg('writing address')
    address = artworkData['address']
    font = axi.Font(axi.FUTURAL, 14)
    y = 2.175
    paths = []
    for line in address:
        if len(line) != 0:
            opts.dbg('writing', line)
            d = font.wrap(unidecode(line), 3, 0.5, justify=True)  # type: axi.Drawing
            d = d.translate(4.25, y)
            paths += d.paths
        y += 0.5
    if len(paths):
        render_drawing(axi.Drawing(paths), opts=opts)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    filename = sys.argv[1]
    artworkData = json.loads(open(filename, 'r').read())
    write_address(artworkData)
