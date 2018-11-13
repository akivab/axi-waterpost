import axi

def main():
    device = axi.Device()
    device.pen_up()
    device.home()
    device.pen_down()
    device.goto(0, 8)
    device.goto(8, 8)
    device.goto(8, 0)
    device.home()
    device.pen_up()
    device.home()


if __name__ == '__main__':
    main()