import axi
import sys
import json
from unidecode import unidecode


def main(filename):
    data = json.loads(open(filename, 'r').read())
    address = data['address']
    font = axi.Font(axi.FUTURAL, 14)
    y = 2.175
    for line in address:
        print 'writing', line
        d = font.wrap(unidecode(line), 3, 0.5, justify=True)
        d = d.translate(4.25, y)
        axi.draw(d)
        y += 0.5


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'provide input file'
        exit()
    main(sys.argv[1])
