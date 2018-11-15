import pdb
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
    surface_html = None
    surface = None
    if opts.useHtml:
        surface_html = drawing.render_svg(bounds=opts.bounds, rgb=colors.COLOR_RGB[colorTag], surface=opts.surfaceHtml)
    else:
        surface = drawing.render(bounds=opts.bounds, rgb=colors.COLOR_RGB[colorTag], surface=opts.surface)
    if opts and opts.renderPath:
        if (opts.useHtml and not surface_html) or (not opts.useHtml and not surface):
            exit(1)
        if opts.useHtml:
            open(opts.renderPath, 'w').write(surface_html + '</script>')
        else:
            surface.write_to_png(opts.renderPath)
    if opts and opts.shouldExecuteInstructions:
        axi.draw(drawing)
    if opts.addToSurface:
        if opts.useHtml:
            opts.surfaceHtml = surface_html
        else:
            opts.surface = surface
    return surface_html if opts.useHtml else surface

