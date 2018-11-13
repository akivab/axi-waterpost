import axi

BLUE = (10, 0.5)
GREEN = (10, 2.5)
RED = (10, 4)
YELLOW = (12, 0.5)
WATER = (12, 2.5)


def paint_brush(device, tuple):
    device.pen_up()
    device.goto(*tuple)
    turtle = axi.Turtle()
    turtle.circle(0.1, 360 * 10, steps=90)
    axi.draw(turtle.drawing)
    device.pen_up()


def turtle_drawing(deg):
    turtle = axi.Turtle()
    i = 0.1
    while i < 1:
        turtle.pendown()
        turtle.circle(i, -360, steps=90)
        i += 0.05
        turtle.seth(deg)
        turtle.forward(0.1)
        turtle.penup()

    d = turtle.drawing
    d.paths.reverse()
    return d


def font_drawing():
    font = axi.Font(axi.FUTURAL, 100)
    d = font.wrap("UNITA", 8, 0.5, justify=True)
    d = d.center(8, 8)
    d = d.translate(0.05, 0)
    return d


def main():
    device = axi.Device()
    device.pen_up()
    device.home()
    colors = [YELLOW, RED, BLUE, GREEN]
    deg = 30
    i = 0
    while deg <= 360:
        paint_brush(device, colors[i])
        device.pen_up()
        device.goto(4, 4)
        axi.draw(turtle_drawing(deg))
        i = (i + 1) % len(colors)
        deg += 30

    # for i in xrange(10):
    #     axi.draw(d)


if __name__ == '__main__':
    main()
