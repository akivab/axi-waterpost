import pdb
import axi
import colors
from WaterpostOptions import WaterpostOptions, DefaultOpts


def render_drawing(drawing, colorTag=-1, opts=DefaultOpts):
    """
    :type drawing: axi.Drawing
    :type colorTag: int
    :type opts: WaterpostOptions
    :returns cairo.ImageSurface
    """
    surface = drawing.render(bounds=opts.bounds, rgb=colors.COLOR_RGB[colorTag], surface=opts.surface)
    if opts and opts.renderPath:
        if surface is None:
            pdb.set_trace()
            print 'Error!!!'
            exit(1)
        surface.write_to_png(opts.renderPath)
    if opts and opts.shouldExecuteInstructions:
        axi.draw(drawing)
    return surface
