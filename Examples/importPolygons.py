#!/usr/bin/python3
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import gcode_lib

# ------------------------------------------------------------------------------
                                                           # drilling parameters
machining_parameters = gcode_lib.default_machining_parameters
machining_parameters['drill_depth'] = 2
machining_parameters['pass_depth']  = 1

# ------------------------------------------------------------------------------
                                                            # input polygon spec
polygon1_name = 'gear'
polygon2_name = 'star'
polygon_file_name = 'logo.svg'
polygon_file_name = current_dir + os.sep + polygon_file_name

# ------------------------------------------------------------------------------
                                                              # output file spec
(g_code_file_path, g_code_file_name) = os.path.split(__file__)
g_code_file_path = g_code_file_path.rstrip('./')
design_name = g_code_file_name.replace('.py', '')
g_code_file_name = g_code_file_path + os.sep + design_name + '.gcode'

# ------------------------------------------------------------------------------
                                                                       # display
INDENT = 2 * ' '

# ==============================================================================
                                                                   # main script
print('Polygon import example')
                                                           # write g-code header
print(INDENT + "writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                            # star shape polygon
print(INDENT + 'reading from %s' % polygon_file_name)

comment = "polygon \"%s\"" % polygon1_name
print(INDENT + comment)
polygon = gcode_lib.flip_vertical(
    gcode_lib.import_polygon(polygon_file_name, polygon1_name)
)
(x_min, y_min, x_max, y_max) = gcode_lib.min_max(polygon)
polygon = gcode_lib.offset_polygon(polygon, -x_min, -y_min)
(x_offset, y_offset, polygon) = gcode_lib.extract_offset(polygon)
g_code_file.write(gcode_lib.build_drawing_element(
    gcode_lib.polygon_gcode(polygon), x_offset, y_offset,
    machining_parameters,
    comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())


# ------------------------------------------------------------------------------
                                                            # gear shape polygon
print(INDENT + 'reading from %s' % polygon_file_name)

comment = "polygon \"%s\"" % polygon2_name
print(INDENT + comment)
polygon = gcode_lib.flip_vertical(
    gcode_lib.import_polygon(polygon_file_name, polygon2_name)
)
polygon = gcode_lib.offset_polygon(polygon, -x_min, -y_min)
(x_offset, y_offset, polygon) = gcode_lib.extract_offset(polygon)
g_code_file.write(gcode_lib.build_drawing_element(
    gcode_lib.polygon_gcode(polygon), x_offset, y_offset,
    machining_parameters,
    comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
