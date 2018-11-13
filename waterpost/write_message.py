import axi
import sys
import json
from unidecode import unidecode


def main(filename):
    d = get_drawing(filename)
    axi.draw(d)

def get_drawing(filename):
    data = json.loads(open(filename, 'r').read())
    message = unidecode(data['message'])
    print 'writing', message
    font = axi.Font(axi.FUTURAL, 16)
    d = font.wrap(message, 2.5)
    d = d.translate(0.5, 0.5)
    d = d.remove_paths_outside(3.5, 3.5)
    return d

def get_message_height(filename):
    d = get_drawing(filename)
    return d.height + 0.5

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    main(sys.argv[1])
