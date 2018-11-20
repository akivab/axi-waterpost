import axi
from WaterpostOptions import WaterpostOptions, DefaultOpts

COLORS_ROW_1 = 9.2
COLORS_ROW_2 = 11
COLORS_COL_1 = 0
COLORS_COL_2 = 1.4
COLORS_COL_3 = 2.8
COLORS_COL_4 = 4.2
COLORS_COL_5 = 6
COLORS_COL_6 = 7.5


class Color():
    WARM_COLORS = 0
    COOL_COLORS = 1
    DARK_COLORS = 2

    def __init__(self, name=None, index=0, position=None, colorGroup=None, rgb=None):
        self.index = index
        self.name = name
        self.position = position
        self.colorGroup = colorGroup
        self.rgb = rgb

COLORS = [
    Color('GREEN', 0, (COLORS_ROW_1, COLORS_COL_1), colorGroup=Color.COOL_COLORS, rgb=(0,1,0)),
    Color('BLUE', 1, (COLORS_ROW_1, COLORS_COL_2), colorGroup=Color.COOL_COLORS, rgb=(0,0,1)),
    Color('PURPLE', 2, (COLORS_ROW_1, COLORS_COL_3), colorGroup=Color.COOL_COLORS, rgb=(0.5,0,1)),
    Color('BLACK', 3, (COLORS_ROW_1, COLORS_COL_4), colorGroup=Color.DARK_COLORS, rgb=(0,0,0)),
    Color('YELLOW', 4, (COLORS_ROW_2, COLORS_COL_1), colorGroup=Color.WARM_COLORS, rgb=(1,1,0)),
    Color('ORANGE', 5, (COLORS_ROW_2, COLORS_COL_2), colorGroup=Color.WARM_COLORS, rgb=(1,0.5,0)),
    Color('RED', 6, (COLORS_ROW_2, COLORS_COL_3), colorGroup=Color.WARM_COLORS, rgb=(1,0,0)),
    Color('BROWN', 7, (COLORS_ROW_2, COLORS_COL_4), colorGroup=Color.DARK_COLORS, rgb=(0,1,0)),
]

WATERS = {
    Color.WARM_COLORS: (COLORS_ROW_1, COLORS_COL_5),
    Color.COOL_COLORS: (COLORS_ROW_2, COLORS_COL_5),
    Color.DARK_COLORS: (COLORS_ROW_1, COLORS_COL_6)
}

def color_brush(tagName, lastColorTagName=0, dipInWater=True, opts=DefaultOpts):
    """
    :type tagName: int
    :type dipInWater: bool
    :type opts: WaterpostOptions
    :param tagName: the name of the color (see color order)
    :param dipInWater: whether to dip brush in water before painting
    :return: None
    """
    if not opts.shouldExecuteInstructions:
        print 'Coloring brush {}'.format(tagName)
        return
    if tagName < 0 or tagName >= len(COLORS):
        raise Exception('tag name bad: ', tagName)
    device = axi.Device()
    device.pen_up()
    color_tuple = COLORS[tagName].position
    turtle = axi.Turtle()
    turtle.circle(0.1, 360 * 5, steps=90)

    if dipInWater:
        water = WATERS[COLORS[lastColorTagName].colorGroup]
        device.goto(*water)
        axi.draw(turtle.drawing)

    device.pen_up()
    device.goto(*color_tuple)
    axi.draw(turtle.drawing)

    device.pen_up()
    device.home()


def getRgbForTag(colorTag):
    return COLORS[colorTag].rgb