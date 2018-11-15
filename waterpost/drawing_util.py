import axi

import colors
from WaterpostOptions import WaterpostOptions, DefaultOpts


def render_drawing(drawing, colorTag=-1, opts=DefaultOpts):
    """
    :param addToSurface: bool
    :type drawing: axi.Drawing
    :type colorTag: int
    :type opts: WaterpostOptions
    :returns cairo.ImageSurface
    """
    opts.surface = drawing.render(bounds=opts.bounds, rgb=colors.COLOR_RGB[colorTag], surface=opts.surface)
    if opts and opts.renderPath and opts.surface:
            opts.surface.write_to_png(opts.renderPath)
    if opts and opts.shouldExecuteInstructions:
        axi.draw(drawing)
