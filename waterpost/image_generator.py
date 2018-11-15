import tempfile
import draw_artwork, write_message, write_address, draw_signature
from WaterpostOptions import WaterpostOptions
import sys
import json


def generate_artwork_from_json(json_file):
    suffix = ".png"
    front_of_card = tempfile.NamedTemporaryFile(suffix=suffix).name
    options = WaterpostOptions(renderPath=front_of_card, shouldExecuteInstructions=False, debug=False)
    draw_artwork.draw_artwork(json_file, opts=options)

    back_of_card = tempfile.NamedTemporaryFile(suffix=suffix).name
    options = WaterpostOptions(renderPath=None, shouldExecuteInstructions=False, debug=False)
    options.addToSurface = True
    draw_signature.draw_signature(json_file, options)
    write_message.write_message(json_file, options)
    options.renderPath = back_of_card
    write_address.write_address(json_file, options)
    print '{}\n{}\n'.format(front_of_card, back_of_card)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    filename = sys.argv[1]
    artworkData = json.loads(open(filename, 'r').read())
    generate_artwork_from_json(artworkData)
