#!/usr/bin/python3
import os
import argparse
import sys
import re

# ==============================================================================
# Constants
#
inch_to_mm = 25.4
inch_to_px = 96
mm_to_px = inch_to_px/inch_to_mm  # ~ 3.7795
displacement_line_width = 1

INDENT = 2 * ' '

# ==============================================================================
# Command line arguments
#
                                                             # specify arguments
parser = argparse.ArgumentParser(
  description='creates an SVG representation a g-code file'
)
                                                                   # g-code file
parser.add_argument('gcodeFile')
                                                                    # page width
parser.add_argument(
    '-x', '--width', default=1000,
    help = 'page width in mm'
)
                                                                   # page height
parser.add_argument(
    '-y', '--height', default=1000,
    help = 'page height in mm'
)
                                                                # drill diameter
parser.add_argument(
    '-d', '--diameter', default=1/4*inch_to_mm,
    help = 'default drill diameter in mm'
)
                                                               # plate thickness
parser.add_argument(
    '-t', '--thickness', default=20,
    help = 'board thickness in mm'
)
                                                                # verbose output
parser.add_argument(
    '-v', '--verbose', action='store_true',
    help = 'verbose display'
)
                                                             # process arguments
parser_arguments = parser.parse_args()

script_directory = os.path.dirname(os.path.realpath(__file__))
gcode_file_spec = parser_arguments.gcodeFile
if not os.path.isfile(gcode_file_spec) :
    gcode_file_spec = os.sep.join([script_directory, gcode_file_spec])
page_width = int(parser_arguments.width)
page_height = int(parser_arguments.height)
drill_diameter = float(parser_arguments.diameter)
plate_thickness = float(parser_arguments.thickness)
verbose = parser_arguments.verbose

svg_file_spec = '.'.join(gcode_file_spec.split('.')[:-1]) + '.svg'
drill_line_width = drill_diameter

# ------------------------------------------------------------------------------
                                                                     # functions
# ..............................................................................
                                  # dertemine new coordinates after displacement
def new_coordinates(code, absolute_mode,
    old_x, old_y, old_z,
    origin_x, origin_y, origin_z
):
                                                       # values if not specified
    if absolute_mode :
        x = old_x - origin_x
        y = old_y - origin_y
        z = old_z - origin_z
    else :
        x = 0
        y = 0
        z = 0
                                              # extract coordinates if specified
    for part in code:
        if part[0] == 'X':
            x = float(part[1:])
        if part[0] == 'Y':
            y = float(part[1:])
        if part[0] == 'Z':
            z = float(part[1:])
                                                      # add corresponding offset
    if absolute_mode:
        x = origin_x + x
        y = origin_y + y
        z = origin_z + z
    else:
        x = old_x + x
        y = old_y + y
        z = old_z + z

    return(x, y, z)

# ..............................................................................
                                                         # color for drill depth
def color_code(z):
    color = 'green'
    if z == 0 :
        color = 'orange'
    elif z < 0 :
        if z >= -plate_thickness :
            intensity = 255 + z*255/plate_thickness
            color = "rgb(%d, %d, %d)" % tuple(intensity*i for i in (1, 1, 1))
        else :
            color = 'black'

    return(color)

# ..............................................................................
                                           # add layer name in front of SVG code
def addd_layer_name(code, z):
    layer_depth = "%06.3f" % -z
    layer_depth = layer_depth.rstrip('0')
    layer_depth = layer_depth.rstrip('.')
    if layer_depth == '-0' :
        layer_depth = '0'

    code = "depth_%s %s" % (layer_depth, code)

    return(code)

# ..............................................................................
                                                  # SVG code for drilling a hole
def drill_hole(x, y, z):
                                                                  # build vector
    svg_code = '<circle'
    svg_code += " cx=\"%d\"" % (mm_to_px*x)
    svg_code += " cy=\"%d\"" % (mm_to_px*(page_height-y))
    svg_code += " r=\"%.3f\"" % (mm_to_px*drill_diameter/2)
    svg_code += " stroke=\"none\" fill=\"%s\"" % color_code(z)
    svg_code += ' />'
                                                                # add layer name
    svg_code = addd_layer_name(svg_code, z)

    return(svg_code)

# ..............................................................................
                                            # SVG code for drilling displacement
def drill_line(x1, y1, x2, y2, z):
                                                                  # build vector
    svg_code = '<line'
    svg_code += " x1=\"%.3f\"" % (mm_to_px*x1)
    svg_code += " y1=\"%.3f\"" % (mm_to_px*(page_height-y1))
    svg_code += " x2=\"%.3f\"" % (mm_to_px*x2)
    svg_code += " y2=\"%.3f\"" % (mm_to_px*(page_height-y2))
    svg_code += " stroke=\"%s\"" % color_code(z)
    svg_code += " stroke-width=\"%.3f\"" % (mm_to_px*drill_line_width)
    svg_code += " stroke-linecap=\"round\""
    svg_code += ' />'
                                                                # add layer name
    svg_code = addd_layer_name(svg_code, z)

    return(svg_code)

# ..............................................................................
                                          # SVG code for in the air displacement
def displacement_line(x1, y1, x2, y2, z):
                                                                  # build vector
    svg_code = '<line'
    svg_code += " x1=\"%.3f\"" % (mm_to_px*x1)
    svg_code += " y1=\"%.3f\"" % (mm_to_px*(page_height-y1))
    svg_code += " x2=\"%.3f\"" % (mm_to_px*x2)
    svg_code += " y2=\"%.3f\"" % (mm_to_px*(page_height-y2))
    svg_code += " stroke=\"%s\"" % color_code(z)
    svg_code += " stroke-width=\"%.3fmm\"" % displacement_line_width
    svg_code += ' />'
                                                                # add layer name
    svg_code = 'displacements ' + svg_code

    return(svg_code)

# ------------------------------------------------------------------------------
                                                                   # main script
print("Reading \"%s\"" % gcode_file_spec)
absolute_mode = True
origin_x = 0
origin_y = 0
origin_z = 0
old_x = 0
old_y = 0
old_z = 0
new_x = 0
new_y = 0
new_z = 0
vector_list = []
                                                              # loop on commands
with open(gcode_file_spec) as gcode_file:
    for line in gcode_file:
        code = line.rstrip().upper()
        while ('(' in code) :
            code = re.sub('\s*\(.*\)', '', code)
        # print(code)
        draw_move = False
        if code != '' :
            code_elements = code.split()
            # print(code_elements[0])
                                                                # drill diameter
            if code_elements[0][0] == 'T' :
                # print('T : tool')
                drill_diameter = float(code_elements[0][1:]) # * inch_to_mm
                drill_line_width = drill_diameter
                                                    # set position as new origin
            if code_elements[0] == 'G92' :
                # print('G92 : origin')
                (origin_x, origin_y, origin_z) = new_coordinates(
                    code_elements[1:], absolute_mode,
                    old_x, old_y, old_z,
                    origin_x, origin_y, origin_z
                )
                                                        # absolute/relative mode
            if code_elements[0] == 'G90' :
                # print('G90 : absolute')
                absolute_mode = True
            if code_elements[0] == 'G91' :
                # print('G91 : relative')
                absolute_mode = False
                                                            # find displacements
            if code_elements[0] == 'G0' :
                # print('G0 : move')
                (new_x, new_y, new_z) = new_coordinates(
                    code_elements[1:], absolute_mode,
                    old_x, old_y, old_z,
                    origin_x, origin_y, origin_z
                )
                draw_move = True
            if code_elements[0] == 'G1' :
                # print('G1 : move')
                (new_x, new_y, new_z) = new_coordinates(
                    code_elements[1:], absolute_mode,
                    old_x, old_y, old_z,
                    origin_x, origin_y, origin_z
                )
                draw_move = True
            # print(draw_move)
                                                            # draw displacements
        if draw_move :
                                                             # draw displacement
            if new_z == old_z :
                if new_z <= 0 :
                    vector = drill_line(old_x, old_y, new_x, new_y, new_z)
                    vector_list.append(vector)
                else :
                    vector = displacement_line(old_x, old_y, new_x, new_y, new_z)
                    vector_list.append(vector)
                                                               # draw drill hole
            else :
                if new_z <= 0 :
                    vector = drill_hole(new_x, new_y, new_z)
                    vector_list.append(vector)
                                                        # update old coordinates
            old_x = new_x
            old_y = new_y
            old_z = new_z
                                                                 # init SVG file
if verbose :
    print()
print("Writing file \"%s\"" % svg_file_spec)
svg_file = open(svg_file_spec, "w")
svg_file.write("<svg\n")
svg_file.write(
    INDENT + "width=\"%dmm\" height=\"%dmm\"\n" % (page_width, page_height)
)
svg_file.write(
    INDENT + "viewBox=\"0 0 %g %g\"\n" % (
        page_width*mm_to_px, page_height*mm_to_px
    )
)
svg_file.write(">\n")
                                                   # set Inkscape units and grid
svg_file.write(
    INDENT + "<sodipodi:namedview\n" +
    2*INDENT + "inkscape:document-units=\"cm\"\n" +
    2*INDENT + "showgrid=\"true\"\n" +
    INDENT + ">\n" +
    2*INDENT + "<inkscape:grid\n" +
    3*INDENT + "type=\"xygrid\"\n" +
    3*INDENT + "id=\"cm\"\n" +
    3*INDENT + "units=\"cm\"\n" +
    3*INDENT + "spacingx=\"%g\"\n" % (10*mm_to_px) +
    3*INDENT + "spacingy=\"%g\"\n" % (10*mm_to_px) +
    3*INDENT + "emspacing=\"10\"\n" +
    3*INDENT + "originx=\"0\"\n" +
    3*INDENT + "originy=\"0\"\n" +
    2*INDENT + "/>\n" +
    INDENT + "</sodipodi:namedview>\n"
)

                                                              # build layer list
layer_list = []
for vector in vector_list :
    layer = vector.split()[0]
    if layer not in layer_list :
        layer_list.append(layer)
layer_list.sort(reverse=True)
                                               # group and write vectors to file
for layer in layer_list :
    if verbose :
        print(INDENT + layer)
    svg_file.write(INDENT + "<g\n")
    svg_file.write(2*INDENT + "inkscape:groupmode=\"layer\"\n")
    svg_file.write(2*INDENT + "id=\"%s\"\n" % layer)
    svg_file.write(2*INDENT + "inkscape:label=\"%s\"\n" %layer)
    svg_file.write(INDENT + ">\n")
    for vector in vector_list :
        vector_layer = vector.split()[0]
        if vector_layer == layer :
            vector = vector.split(' ', 1)[1]
#            print(2*INDENT + vector)
            svg_file.write(2*INDENT + vector + "\n")
    svg_file.write(INDENT + "</g>\n")
                                                            # terminate SVG file
svg_file.write("</svg>\n")
svg_file.close()
