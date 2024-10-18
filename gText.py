#!/usr/bin/python3
import math
import gcode_lib

# ------------------------------------------------------------------------------
                                                           # drilling parameters
letter_machining_parameters = gcode_lib.default_machining_parameters
letter_displacement_speeds = gcode_lib.default_displacement_speeds

half_circle_facet_nb = 8
quarter_circle_facet_nb = round(half_circle_facet_nb/2)
lift_for_drill_back = False

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
    bore_speed = displacement_speeds[
        gcode_lib.drill_bore_speed_id
    ]
    g_code = ''
                                                                            # t1
    if line_specification == 't1' :
        g_code = gcode_lib.move_steady(
            2*drill_diameter, 0, 0, drill_speed
        )
                                                                            # t2
    if line_specification == 't2' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(-drill_diameter, 0, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(-drill_diameter, 0, 0, drill_speed)
                                                                            # t3
    if line_specification == 't3' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(0, 3*drill_diameter, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(0, 3*drill_diameter, 0, drill_speed)
                                                                            # t4
    if line_specification == 't4' :
        g_code = gcode_lib.move_steady(
            0, 6.5*drill_diameter, 0, drill_speed
        )
                                                                            # t4
    if line_specification == 't5' :
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
    if character == 't' :
        line_set = ['t1', 't2', 't3', 't4', 't5']
        entry_point = [0, 5]
        exit_point  = [2.5, 0]

    return(line_set, entry_point, exit_point)

# ..............................................................................
                                                    # g-code set for a character
def build_character_g_code(
    character,
    machining_parameters=letter_machining_parameters,
    displacement_speeds=letter_displacement_speeds,
    lift_for_drill_back=False
) :
    g_code = "; %s\n" % character
    (line_set, entry_point, exit_point) = build_line_set(character)
    for line in line_set :
        g_code += build_line_g_code(
            line,
            letter_machining_parameters, letter_displacement_speeds,
            lift_for_drill_back
        )
    return(g_code)

# ==============================================================================
                                                                   # main script
print('Testing g-codes for drilling text')
test_string = 'the quick brown fox jumps over the lazy dog'

drill_tool_diameter = letter_machining_parameters[gcode_lib.drill_diameter_id]
g_code = gcode_lib.select_tool(drill_tool_diameter)
for character in test_string[:1] :
    print(character)
    g_code += build_character_g_code(
        character,
        letter_machining_parameters, letter_displacement_speeds,
        lift_for_drill_back
    )
    print(g_code)
