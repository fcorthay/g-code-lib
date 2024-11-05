#!/usr/bin/python3
import os
import sys
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
import gcode_lib
import text_lib

# ------------------------------------------------------------------------------
                                                                   # test string
pangram = 'The quick brown fox jumps over the lazy dog'
digits = '0123456789' + ' ' + '+-*/\'().,:'
lift_for_drill_back = False

# ------------------------------------------------------------------------------
                                                                # font file spec
font_file_spec = parent_dir + os.sep + 'text-rounded.txt'
font_file_spec = parent_dir + os.sep + 'text-squared.txt'

# ------------------------------------------------------------------------------
                                                           # drilling parameters
machining_parameters = gcode_lib.default_machining_parameters
machining_parameters['drill_diameter'] = 2
machining_parameters['pass_depth']  = 1

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
print('Text drilling example')
                                                           # write g-code header
print(INDENT + "writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=machining_parameters
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                # lowercase text
comment = 'lowercase text'
g_code_file.write(";\n; %s\n;\n" % comment)
print(INDENT + comment)
text = pangram
g_code_file.write(text_lib.line_g_code(
    text, font_file_spec, machining_parameters, lift_for_drill_back
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                # uppercase text
comment = 'uppercase text'
g_code_file.write(";\n; %s\n;\n" % comment)
print(INDENT + comment)
g_code_file.write(gcode_lib.move_fast(
    0, 3*text_lib.lc_letter_height*machining_parameters['drill_diameter'], 0,
    machining_parameters['fast_displacement_speed']
))
text = pangram.upper()
g_code_file.write(text_lib.line_g_code(
    text, font_file_spec, machining_parameters, lift_for_drill_back
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                        # digits
comment = 'digits'
g_code_file.write(";\n; %s\n;\n" % comment)
print(INDENT + comment)
g_code_file.write(gcode_lib.move_fast(
    0, 6*text_lib.lc_letter_height*machining_parameters['drill_diameter'], 0,
    machining_parameters['fast_displacement_speed']
))
text = digits
g_code_file.write(text_lib.line_g_code(
    text, font_file_spec, machining_parameters, lift_for_drill_back
))
                                                                # back to origin
g_code_file.write(gcode_lib.move_back_to_origin())

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
