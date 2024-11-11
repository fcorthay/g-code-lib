#!/usr/bin/python3
import os
import math
import re
import gcode_lib

# ------------------------------------------------------------------------------
                                                             # letter parameters
drill_diameter = 2
letter_spacing = 2
space_spacing = 4

lc_letter_width = 3
lc_letter_height = 5
lc_circle_radius = lc_letter_width/2
small_circle_radius = lc_letter_width/3

uc_letter_width = 4
uc_letter_height = 8
uc_circle_radius = uc_letter_width/2

LIFT_UP = True
LIFT_DISPLACEMENT_HEIGHT = True

# ------------------------------------------------------------------------------
                                                           # drilling parameters
letter_machining_parameters = gcode_lib.default_machining_parameters
letter_machining_parameters['drill_diameter'] = drill_diameter

pass_depth  = letter_machining_parameters['pass_depth']
move_speed  = letter_machining_parameters['fast_displacement_speed']
drill_speed = letter_machining_parameters['drill_displacement_speed']
bore_speed  = letter_machining_parameters['drill_bore_speed']

half_circle_facet_nb = 16
quarter_circle_facet_nb = round(half_circle_facet_nb/2)
short_circle_final_y_offset = 1/2
short_circle_angle_takeback = math.atan2(
    short_circle_final_y_offset, lc_circle_radius
)
short_circle_final_x_offset = \
    lc_circle_radius*(1 - math.cos(short_circle_angle_takeback))

# ------------------------------------------------------------------------------
                                                                       # display
INDENT = 2 * ' '

# ==============================================================================
                                                               # letters g-codes

# ..............................................................................
                                                                 # vertical line
def move_diagonal(
    x_displacement, y_displacement,
    machining_parameters=letter_machining_parameters
) :
    g_code = gcode_lib.move_steady(
        x_displacement*machining_parameters['drill_diameter'],
        y_displacement*machining_parameters['drill_diameter'],
        0,
        machining_parameters['drill_displacement_speed']
    )

    return (g_code)

# ..............................................................................
                                                               # horizontal line
def move_horizontal(
    displacement, machining_parameters=letter_machining_parameters
) :
    g_code = move_diagonal(displacement, 0, machining_parameters)

    return (g_code)

# ..............................................................................
                                                                 # vertical line
def move_vertical(
    displacement, machining_parameters=letter_machining_parameters
) :
    g_code = move_diagonal(0, displacement, machining_parameters)

    return (g_code)

# ..............................................................................
                                                            # vertical move back
def lift_drill(
    lift_up=LIFT_UP,
    machining_parameters=letter_machining_parameters,
    lift_displacement_height = False
) :
    z_displacement = machining_parameters['pass_depth']
    if lift_displacement_height :
        z_displacement = machining_parameters['displacement_height']
    if not lift_up :
        z_displacement = -z_displacement

    g_code = gcode_lib.move_steady(
        0, 0, z_displacement,
        machining_parameters['drill_bore_speed']
    )

    return (g_code)

# ..............................................................................
                                                            # diagonal move back
def move_back_diagonal(
    x_displacement, y_displacement,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
    if lift_for_drill_back :
        g_code = lift_drill(LIFT_UP, machining_parameters)
        g_code += gcode_lib.move_fast(
            x_displacement*machining_parameters['drill_diameter'],
            y_displacement*machining_parameters['drill_diameter'],
            0,
            machining_parameters['fast_displacement_speed']
        )
        g_code += gcode_lib.move_fast(
            x_displacement*drill_diameter, y_displacement*drill_diameter,
            0, move_speed
        )
        g_code = lift_drill(not LIFT_UP, machining_parameters)
    else :
        g_code = gcode_lib.move_steady(
            x_displacement*machining_parameters['drill_diameter'],
            y_displacement*machining_parameters['drill_diameter'],
            0,
            machining_parameters['drill_displacement_speed']
        )

    return (g_code)

# ..............................................................................
                                                                # usual size arc
def move_arc(
    radius,
    start_angle, end_angle,
    machining_parameters=letter_machining_parameters,
    facet_nb=half_circle_facet_nb
) :
    g_code = gcode_lib.circle_arc_gcode(
        radius*machining_parameters['drill_diameter'], facet_nb,
        start_angle, end_angle,
        machining_parameters['drill_displacement_speed']
    )

    return (g_code)

# ..............................................................................
                                                    # g-code set for a character
def line_set_to_gcode(
    line_set,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
    entry_point = [0, 0]
    max_x = 0
    exit_point_x = 0
    exit_point_y = 0
    exit_point = [0, 0]
    g_code = ''
                                                             # split to commands
    commands = re.findall(r'[a-zA-Z]', line_set)
    parameters = re.split(r'\s*[a-zA-Z]\s*', line_set)[1:]
                                                            # interpret commands
    for index in range(len(commands)) :
        command = commands[index]
        parameter_list = re.split(r'\s+', parameters[index])
        delta_x = 0
        delta_y = 0
        if (index == 0) and (command == 'm') :
                                                         # first command is move
            delta_x = float(parameter_list[0])
            delta_y = float(parameter_list[1])
            entry_point = [delta_x, delta_y]
        else :
                                                               # horizontal line
            if command == 'h' :
                delta_x = float(parameter_list[0])
                g_code += move_horizontal(delta_x, machining_parameters)
                                                                 # vertical line
            elif command == 'v' :
                delta_y = float(parameter_list[0])
                g_code += move_vertical(delta_y, machining_parameters)
                                                                 # diagonal line
            elif command == 'l' :
                delta_x = float(parameter_list[0])
                delta_y = float(parameter_list[1])
                g_code += move_diagonal(delta_x, delta_y, machining_parameters)
                                                           # (diagonal) movement
            elif command == 'm' :
                if (index > 0) and (commands[index-1] != 'm') :
                    if lift_for_drill_back :
                        g_code += lift_drill(LIFT_UP, machining_parameters)
                delta_x = float(parameter_list[0])
                delta_y = float(parameter_list[1])
                g_code += move_diagonal(delta_x, delta_y, machining_parameters)
                if (index-1 < len(commands)) and (commands[index+1] != 'm') :
                    if lift_for_drill_back :
                        g_code += lift_drill(not LIFT_UP, machining_parameters)
                                                                    # circle arc
            elif command == 'a' :
                radius      = float(parameter_list[0])
                start_angle = float(parameter_list[1])*math.pi/180
                end_angle   = float(parameter_list[2])*math.pi/180
                delta_x = radius*(math.cos(end_angle) - math.cos(start_angle))
                delta_y = radius*(math.sin(end_angle) - math.sin(start_angle))
                if                                             \
                    ((start_angle < 0) and (end_angle > 0)) or \
                    ((start_angle > 0) and (end_angle < 0))    \
                :
                    max_x_at_0 = exit_point_x + radius
                    if max_x_at_0 > max_x :
                        max_x = max_x_at_0
                g_code += move_arc(
                    radius, start_angle, end_angle, machining_parameters
                )
                                                                 # lift drill up
            elif command == 'u' :
                g_code += lift_drill(
                    LIFT_UP, machining_parameters, LIFT_DISPLACEMENT_HEIGHT
                )
                                                               # dive drill down
            elif command == 'd' :
                g_code += lift_drill(
                    not LIFT_UP, machining_parameters, LIFT_DISPLACEMENT_HEIGHT
                )
                                                             # update exit point
        exit_point_x = exit_point_x + delta_x
        exit_point_y = exit_point_y + delta_y
        if exit_point_x > max_x :
            max_x = exit_point_x
                                                                    # exit point
    exit_point = [exit_point_x - max_x, exit_point_y]

    return(g_code, entry_point, exit_point)

# ..............................................................................
                                                    # g-code set for a character
def character_data(
    character, font_dictionary,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
    g_code = ''
    entry_point = [0, 0]
    exit_point  = [0, 0]
                                                               # get information
    line_set = []
    if character in font_dictionary :
        line_set = font_dictionary[character]
    if line_set :
                                                                       # comment
        if character == '(' :
            g_code = "; opening parenthesis\n"
        elif character == ')' :
            g_code = "; closing parenthesis\n"
        else :
            g_code = "; %s\n" % character
                                                                     # dive down
        g_code += lift_drill(not LIFT_UP, machining_parameters)
                                                                   # drill lines
        (character_g_code, entry_point, exit_point) = line_set_to_gcode(
            line_set, machining_parameters, lift_for_drill_back
        )
        g_code += character_g_code
                                                                  # lift back up
        g_code += lift_drill(LIFT_UP, machining_parameters)

    return(g_code, entry_point, exit_point)

# ------------------------------------------------------------------------------
def line_g_code(
    line, font_file_spec,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
                                                             # write line g-code
    drill_tool_diameter = machining_parameters['drill_diameter']
    text_g_code = gcode_lib.select_tool(drill_tool_diameter)
                                                              # drill characters
    font_information = open(font_file_spec, 'r').read().split("\n")
    font_dictionary = {}
    for character_information in font_information :
        if character_information.startswith(':') :
            character = ':'
            line_set = re.sub(r'\:\s*\:\s*', '', character_information)
            font_dictionary[character] = line_set
        elif ':' in character_information :
            [character, line_set] = re.split(r'\s*:\s*', character_information)
            if character.startswith('\\') :
              character = character[1]
#            print(character)
#            print(line_set)
            font_dictionary[character] = line_set
    displacement_height = machining_parameters['displacement_height']
    drill_diameter      = machining_parameters['drill_diameter']
    displacement_speed  = machining_parameters['fast_displacement_speed']
    old_exit_point = [letter_spacing, 0]
    for character in line :
        if character == ' ' :
                                              # add offset for character spacing
            old_exit_point[0] = old_exit_point[0] \
                - (space_spacing - letter_spacing)
        else :
                                                            # get character data
            (char_g_code, entry_point, exit_point) = character_data(
                character, font_dictionary,
                letter_machining_parameters,
                lift_for_drill_back
            )
                                                       # move to character start
            text_g_code += gcode_lib.move_fast(
                drill_diameter*(
                    entry_point[0] - old_exit_point[0] + letter_spacing
                ),
                drill_diameter*(entry_point[1] - old_exit_point[1]),
                0,
                displacement_speed
            )
                                                            # go down to surface
            text_g_code += gcode_lib.move_fast(
                0, 0, -displacement_height, displacement_speed
            )
                                                               # drill character
            text_g_code += char_g_code
                                               # go up for the next displacement
            text_g_code += gcode_lib.move_fast(
                0, 0,  displacement_height, displacement_speed
            )
        old_exit_point = exit_point

    return(text_g_code)
