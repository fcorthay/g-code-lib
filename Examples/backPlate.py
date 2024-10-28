#!/usr/bin/python3
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import gcode_lib

# ------------------------------------------------------------------------------
                                                                      # geometry
box_length = 210
box_width  = 142
box_height  = 80

drill_diameter = 4
board_thickness = 6
board_drill_depth = board_thickness + 1

back_board_length   = box_length
back_board_width    = box_height - 2*board_thickness

back_board_x_offset = 0
back_board_y_offset = 0

back_fixing_holes_x_offset = 3
back_fixing_holes_y_offset = 4
back_fixing_holes_length = 204
back_fixing_holes_width = 60

rpi_slit_length = 58
rpi_slit_width = 18
rpi_slit_x_offset = back_board_length - rpi_slit_length - 7
rpi_slit_y_offset = 30

power_supply_slit_length = 28
power_supply_slit_width = 60
power_supply_slit_x_offset = back_board_length - power_supply_slit_length - 156
power_supply_slit_y_offset = 4

banana_plugs_diameter = 12 - drill_diameter
banana_plugs_x_offset = back_board_length + banana_plugs_diameter/2 \
	- drill_diameter/2 - 95
banana_plugs_y_offset = 19 - drill_diameter/2
banana_plugs_x_nb = 2
banana_plugs_y_nb = 2
banana_plugs_x_spacing = 25
banana_plugs_y_spacing = 25

# ------------------------------------------------------------------------------
                                                           # drilling parameters
machining_parameters = {
    'displacement_height'      : 10,
    'drill_depth'              : board_drill_depth,
    'pass_depth'               : 1,
    'drill_diameter'           : drill_diameter,
    'fast_displacement_speed'  : 1000,
    'drill_displacement_speed' : 100,
    'drill_bore_speed'         : 200
}
fast_displacement_speed  = machining_parameters['fast_displacement_speed']
drill_displacement_speed = machining_parameters['drill_displacement_speed']

# ------------------------------------------------------------------------------
                                                                     # file spec
(g_code_file_path, g_code_file_name) = os.path.split(__file__)
g_code_file_path = g_code_file_path.rstrip('./')
design_name = g_code_file_name.replace('.py', '')
g_code_file_name = g_code_file_path + os.sep + design_name + '.gcode'

# ------------------------------------------------------------------------------
                                                                       # display
INDENT = 2 * ' '

# ==============================================================================
                                                                   # main script
print('Building g-codes for the roomAmp bottom, back or top plate')
                                                           # write g-code header
print(INDENT + "Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters,
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                              # back board shape
comment = "shape"
print(INDENT + comment)
g_code_file.write(";\n; %s\n;\n" % comment)
g_code_file.write(gcode_lib.move_fast(
    back_board_x_offset, back_board_y_offset, 0, fast_displacement_speed
))
g_code_file.write(gcode_lib.rectangle_gcode(
    back_board_length, back_board_width, fast_displacement_speed
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                              # back board holes
comment = "fixing holes"
print(INDENT + comment)
                                                                      # hole set
back_fixing_holes = gcode_lib.build_retangle(
    back_fixing_holes_x_offset, back_fixing_holes_y_offset,
    back_fixing_holes_length, back_fixing_holes_width
)
                                                                  # holes g-code
g_code_file.write(gcode_lib.build_hole_set(
    back_fixing_holes,
    machining_parameters,
    "\n; %s\n;" % comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                  # back board connector cutouts
comment = "connection cutouts"
print(INDENT + comment)
                                                                      # RPi slit
comment = "RPi slit"
print(2*INDENT + comment)
g_code_file.write(gcode_lib.build_drawing_element(
    gcode_lib.rectangle_gcode(
        rpi_slit_length - drill_diameter,
        rpi_slit_width - drill_diameter,
        drill_displacement_speed
    ),
    rpi_slit_x_offset + drill_diameter/2,
    rpi_slit_y_offset + drill_diameter/2,
    machining_parameters,
    comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())
                                                             # power supply slit
comment = "power supply slit"
print(2*INDENT + comment)
g_code_file.write(gcode_lib.build_drawing_element(
    gcode_lib.rectangle_gcode(
        power_supply_slit_length - drill_diameter,
        power_supply_slit_width - drill_diameter,
        drill_displacement_speed
    ),
    power_supply_slit_x_offset + drill_diameter/2,
    power_supply_slit_y_offset + drill_diameter/2,
    machining_parameters,
    comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())
                                                                  # banana plugs
comment = "banana plugs"
print(2*INDENT + comment)
g_code_file.write(gcode_lib.move_fast(
    banana_plugs_x_offset + drill_diameter/2,
    banana_plugs_y_offset + drill_diameter/2,
    0,
    fast_displacement_speed
))
for y_index in range(banana_plugs_y_nb) :
    for x_index in range(banana_plugs_x_nb) :
        comment = "banana plug (%d, %d)" % (x_index, y_index)
        g_code_file.write(gcode_lib.build_drawing_element(
            gcode_lib.circle_gcode(
                banana_plugs_diameter
            ),
            0, 0,
            machining_parameters,
            comment
        ))
        if x_index < banana_plugs_x_nb - 1 :
            g_code_file.write(gcode_lib.move_fast(
                -banana_plugs_x_spacing, 0, 0, fast_displacement_speed
            ))
    if y_index < banana_plugs_y_nb - 1 :
        g_code_file.write(gcode_lib.move_fast(
            banana_plugs_x_spacing, banana_plugs_y_spacing, 0,
            fast_displacement_speed
        ))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                    # cut off back plate top end
comment = 'top cut off'
print(INDENT + comment)
g_code_file.write(gcode_lib.build_slit_set(
    -drill_diameter/2, back_board_width + drill_diameter/2,
    back_board_length + drill_diameter, 0, 0, 0, 1,
    machining_parameters,
    "\n; %s\n;" % comment
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
