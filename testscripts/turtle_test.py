import axi


def flower(turtle):
    steps = 0
    i = 0
    while steps < 100:
        mod = i % 5
        x = 128 - mod * mod * mod * 2
        turtle.circle(1, 170)
        turtle.forward(x)
        turtle.circle(20, 200 + mod * mod * 3)
        turtle.forward(x)
        i += 1
        steps += 1

def box(turtle):
    turtle.forward(100)
    turtle.circle(1, 90, steps=90)
    turtle.forward(100)
    turtle.circle(1, 90, steps=90)
    turtle.forward(100)
    turtle.circle(1, 90, steps=90)
    turtle.forward(100)

def main():
    turtle = axi.Turtle()
    box(turtle)
    drawing = turtle.drawing.scale_to_fit(8, 8)
    axi.draw(drawing)


if __name__ == '__main__':
    main()
