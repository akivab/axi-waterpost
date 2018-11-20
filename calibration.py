import axi

def main():
    device = axi.Device()
    device.pen_up()
    device.home()
    device.pen_down()
    device.goto(0, 5)
    device.goto(7, 5)
    device.goto(7, 0)
    device.home()
    device.pen_up()
    device.home()


if __name__ == '__main__':
    main()
