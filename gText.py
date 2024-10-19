#!/usr/bin/python3
import os
import math
import gcode_lib

# ------------------------------------------------------------------------------
                                                           # drilling parameters
letter_spacing = 2
letter_machining_parameters = gcode_lib.default_machining_parameters
letter_displacement_speeds = gcode_lib.default_displacement_speeds

half_circle_facet_nb = 8
quarter_circle_facet_nb = round(half_circle_facet_nb/2)
lift_for_drill_back = False

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
                                                               # letters g-codes

# ..............................................................................
                                                    # g-code set for a character
def build_line_g_code(
    line_specification,
    machining_parameters, displacement_speeds,
    lift_for_drill_back
) :
    drill_diameter = machining_parameters[gcode_lib.drill_diameter_id]
    pass_depth = machining_parameters[gcode_lib.pass_depth_id]
    move_speed = displacement_speeds[gcode_lib.fast_displacement_speed_id]
    drill_speed = displacement_speeds[gcode_lib.drill_displacement_speed_id]
    bore_speed = displacement_speeds[gcode_lib.drill_bore_speed_id]
    g_code = ''
                                                                            # h1
    if line_specification == 'h1' :
        g_code = gcode_lib.move_steady(
            0, -8*drill_diameter, 0, drill_speed
        )
                                                                            # h2
    elif line_specification == 'h2' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(0, 3.5*drill_diameter, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(0, 3.5*drill_diameter, 0, drill_speed)
                                                                            # h3
    elif line_specification == 'h3' :
        g_code = gcode_lib.move_steady(
            3*drill_diameter, 0, 0, drill_speed
        )
                                                                            # h4
    elif line_specification == 'h4' :
        g_code = gcode_lib.move_steady(
            0, -3.5*drill_diameter, 0, drill_speed
        )
                                                                            # t1
    elif line_specification == 't1' :
        g_code = gcode_lib.move_steady(
            2*drill_diameter, 0, 0, drill_speed
        )
                                                                            # t2
    elif line_specification == 't2' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(-drill_diameter, 0, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(-drill_diameter, 0, 0, drill_speed)
                                                                            # t3
    elif line_specification == 't3' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(0, 3*drill_diameter, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(0, 3*drill_diameter, 0, drill_speed)
                                                                            # t4
    elif line_specification == 't4' :
        g_code = gcode_lib.move_steady(
            0, -6.5*drill_diameter, 0, drill_speed
        )
                                                                            # t4
    elif line_specification == 't5' :
        g_code = gcode_lib.circle_arc_gcode(
            1.5*drill_diameter, quarter_circle_facet_nb,
            math.pi, 1.5*math.pi,
            drill_speed
        )

    return(g_code)

# ..............................................................................
                                                   # line set for each character
def build_line_set(character) :
    line_set = []
    entry_point = [0, 0]
    exit_point  = [0, 0]
    if character == 'h' :
        line_set = ['h1', 'h2', 'h3', 'h4']
        entry_point = [0, 8]
        exit_point  = [0, 0]
    elif character == 't' :
        line_set = ['t1', 't2', 't3', 't4', 't5']
        entry_point = [0, 5]
        exit_point  = [0, 0]

    return(line_set, entry_point, exit_point)

# ..............................................................................
                                                    # g-code set for a character
def build_character_g_code(
    character,
    machining_parameters=letter_machining_parameters,
    displacement_speeds=letter_displacement_speeds,
    lift_for_drill_back=False
) :
    pass_depth = machining_parameters[gcode_lib.pass_depth_id]
    bore_speed = displacement_speeds[gcode_lib.drill_bore_speed_id]
                                                                       # comment
    g_code = "; %s\n" % character
                                                                     # dive down
    g_code += gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
                                                                   # drill lines
    (line_set, entry_point, exit_point) = build_line_set(character)
    for line in line_set :
        g_code += build_line_g_code(
            line,
            letter_machining_parameters, letter_displacement_speeds,
            lift_for_drill_back
        )
                                                                  # dive back up
    g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)

    return(g_code, entry_point, exit_point)

# ==============================================================================
                                                                   # main script
print('Testing g-codes for drilling text')
test_string = 'the quick brown fox jumps over the lazy dog'

# ------------------------------------------------------------------------------
                                                           # write g-code header
print(INDENT + "Writing \"%s\"" % g_code_file_name)
g_code_file = open(g_code_file_name, "w")
g_code_file.write(gcode_lib.go_to_start(
    machining_parameters=letter_machining_parameters,
    displacement_speeds=letter_displacement_speeds
))
g_code_file.write(";\n; Test text\n;\n")

# ------------------------------------------------------------------------------
                                                             # write line g-code
drill_tool_diameter = letter_machining_parameters[gcode_lib.drill_diameter_id]
text_g_code = gcode_lib.select_tool(drill_tool_diameter)
                                                            # go down to surface
displacement_height = letter_machining_parameters[
    gcode_lib.displacement_height_id
]
pass_depth = letter_machining_parameters[gcode_lib.pass_depth_id]
drill_diameter = letter_machining_parameters[gcode_lib.drill_diameter_id]
displacement_speed = letter_displacement_speeds[
    gcode_lib.fast_displacement_speed_id
]
text_g_code += gcode_lib.move_fast(
    0, 0, -displacement_height + pass_depth, displacement_speed
)
                                                              # drill characters
old_exit_point = [0, 0]
for character in test_string[:2] :
    print(character)
    (character_g_code, entry_point, exit_point) = build_character_g_code(
        character,
        letter_machining_parameters, letter_displacement_speeds,
        lift_for_drill_back
    )
    text_g_code += gcode_lib.move_fast(
        drill_diameter*(entry_point[0] - old_exit_point[0] + letter_spacing),
        drill_diameter*(entry_point[1] - old_exit_point[1]),
        0,
        displacement_speed
    )
    text_g_code += gcode_lib.move_fast(0, 0, -pass_depth, displacement_speed)
    text_g_code += character_g_code
    text_g_code += gcode_lib.move_fast(0, 0,  pass_depth, displacement_speed)
    old_exit_point = exit_point
g_code_file.write(text_g_code)

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
