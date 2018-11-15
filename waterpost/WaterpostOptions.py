from cairocffi import cairo


class WaterpostOptions:
    renderPath = None  # type: str
    surface = None  # type: cairo.ImageSurface
    shouldExecuteInstructions = False  # type: bool
    debug = True  # type: bool
    bounds = (0, 0, 7, 5)

    def __init__(self, renderPath=None, surface=None, shouldExecuteInstructions=True, debug=False):
        self.renderPath = renderPath
        self.surface = surface
        self.shouldExecuteInstructions = shouldExecuteInstructions
        self.debug = debug

    def dbg(self, *args):
        if self.debug:
            print args


DefaultOpts = WaterpostOptions()
