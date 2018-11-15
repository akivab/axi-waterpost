from cairocffi import cairo


class WaterpostOptions:
    renderPath = None  # type: str
    surface = None  # type: cairo.ImageSurface
    surfaceHtml = None  # type: str
    useHtml = False  # type: bool
    shouldExecuteInstructions = False  # type: bool
    debug = True  # type: bool
    bounds = (0, 0, 7, 5)
    addToSurface = False  # type: bool

    def __init__(self, renderPath=None, surface=None, surfaceHtml=None, useHtml=False, shouldExecuteInstructions=True, debug=False):
        self.addToSurface = False
        self.surfaceHtml = surfaceHtml
        self.useHtml = useHtml
        self.renderPath = renderPath
        self.surface = surface
        self.shouldExecuteInstructions = shouldExecuteInstructions
        self.debug = debug

    def dbg(self, *args):
        if self.debug:
            print args


DefaultOpts = WaterpostOptions()
