import axi
import math
import random

WATER = (10.5, 5)
YELLOW = (9, 5)
BLUE = (9, 3)


def perturb_points(points, deviation):
    result = []
    for x, y in points:
        a = random.random() * 2 * math.pi
        r = random.gauss(0, deviation)
        x += math.cos(a) * r
        y += math.sin(a) * r
        result.append((x, y))
    return result


def star(x, y, r):
    sides = 5
    a = random.random() * 2 * math.pi
    angle = 2 * math.pi / sides
    angles = [angle * i + a for i in range(sides)]
    points = [(x + math.cos(a) * r, y + math.sin(a) * r) for a in angles]
    points = perturb_points(points, 0.1)
    points.append(points[0])
    return points[0::2] + points[1::2]


def clear():
    device = axi.Device()
    device.pen_up()
    x = random.random()
    device.goto(x, 1)
    device.pen_down()
    for i in xrange(5):
        device.goto(x, 1)
        device.goto(x, 0)
    device.pen_up()


def spiral():
    turtle = axi.Turtle()
    size = 0.1
    for i in xrange(20):
        turtle.circle(size * i, -180, 90)
    return turtle.drawing


def main():
    turtle = axi.Turtle()
    device = axi.Device()
    device.enable_motors()
    device.pen_up()
    device.goto(*WATER)
    turtle.circle(0.1, 360 * 5, 90)
    axi.draw(turtle.drawing)
    device.goto(*YELLOW)
    axi.draw(turtle.drawing)
    device.goto(6, 2)
    axi.draw(spiral())
    clear()
    device.disable_motors()


if __name__ == '__main__':
    main()
