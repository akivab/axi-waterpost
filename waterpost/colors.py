import axi

GREEN = (10, 0.5)
YELLOW = (10, 2.25)
RED = (10, 4)
BLUE = (11.5, 0.5)
BLACK = (11.5, 2.25)
WATER = (11.5, 4)

COLOR_ORDER = [GREEN, RED, BLUE, YELLOW, BLACK]
COLOR_RGB = [(0,1,0),(1,0,0),(0,0,1), (1,1,0),(0, 0, 0)]

should_color_brush = True
def color_brush(tagName, dipInWater=True):
    """

    :param tagName: the name of the color (see color order)
    :param dipInWater: whether to dip brush in water before painting
    :return: None
    """
    if not should_color_brush:
        return
    if tagName < 0 or tagName >= len(COLOR_ORDER):
        raise Exception('tag name bad: ', tagName)
    device = axi.Device()
    device.pen_up()
    color_tuple = COLOR_ORDER[tagName]
    turtle = axi.Turtle()
    turtle.circle(0.1, 360 * 5, steps=90)

    if dipInWater:
        device.goto(*WATER)
        axi.draw(turtle.drawing)

    device.pen_up()
    device.goto(*color_tuple)
    axi.draw(turtle.drawing)

    device.pen_up()
    device.home()

