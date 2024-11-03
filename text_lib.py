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
    machining_parameters=letter_machining_parameters
) :
    z_displacement = machining_parameters['pass_depth']
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
                                                            # vertical move back
def move_back_vertical(
    y_displacement,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
    g_code = move_back_diagonal(
        0, y_displacement, machining_parameters, lift_for_drill_back
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
                                                                # usual size arc
def move_arc_2(
    start_angle, end_angle,
    machining_parameters=letter_machining_parameters,
    radius=lc_circle_radius,
    facet_nb=half_circle_facet_nb
) :
    g_code = gcode_lib.circle_arc_gcode(
        radius*machining_parameters['drill_diameter'], facet_nb,
        start_angle, end_angle,
        machining_parameters['drill_displacement_speed']
    )

    return (g_code)

# ..............................................................................
                                                            # quarter circle arc
def move_quarter_arc(
    start_angle, end_angle,
    machining_parameters=letter_machining_parameters,
    radius=lc_circle_radius,
    facet_nb=quarter_circle_facet_nb
) :
    g_code = move_arc_2(
        start_angle, end_angle,
        machining_parameters,
        radius, facet_nb
    )

    return (g_code)

# ..............................................................................
                                                 # quarter of a small circle arc
def move_small_quarter_arc(
    start_angle, end_angle,
    machining_parameters=letter_machining_parameters,
    radius=small_circle_radius,
    facet_nb=quarter_circle_facet_nb
) :
    g_code = move_arc_2(
        start_angle, end_angle,
        machining_parameters,
        radius, facet_nb
    )

    return (g_code)

# ..............................................................................
                                                    # g-code set for a character
def build_line_g_code(
    line_specification,
    machining_parameters,
    lift_for_drill_back
) :
    drill_diameter = machining_parameters['drill_diameter']
    pass_depth     = machining_parameters['pass_depth']
    move_speed     = machining_parameters['fast_displacement_speed']
    drill_speed    = machining_parameters['drill_displacement_speed']
    bore_speed     = machining_parameters['drill_bore_speed']
    g_code = ''
                                                                            # a1
    if line_specification == 'a1' :
        g_code = move_arc_2(
            math.pi - short_circle_angle_takeback, 0, machining_parameters
        )
                                                                            # a2
    elif line_specification == 'a2' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # a3
    elif line_specification == 'a3' :
        g_code = move_back_vertical(
            1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # a4
    elif line_specification == 'a4' :
        g_code = move_arc_2(2*math.pi, math.pi, machining_parameters)
                                                                            # a5
    elif line_specification == 'a5' :
        g_code = move_small_quarter_arc(
            math.pi, math.pi/2, machining_parameters
        )
                                                                            # a6
    elif line_specification == 'a6' :
        g_code = move_horizontal(2, machining_parameters)
                                                                            # b1
    elif line_specification == 'b1' :
        g_code = move_vertical(8, machining_parameters)
                                                                            # b2
    elif line_specification == 'b2' :
        g_code = move_back_vertical(
            -4.5, machining_parameters, lift_for_drill_back
        )
                                                                            # b3
    elif line_specification == 'b3' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # b4
    elif line_specification == 'b4' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # b5
    elif line_specification == 'b5' :
        g_code = move_arc_2(2*math.pi, math.pi, machining_parameters)
                                                                            # c1
    elif line_specification == 'c1' :
        g_code = move_arc_2(
            short_circle_angle_takeback, math.pi, machining_parameters
        )
                                                                            # c2
    elif line_specification == 'c2' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # c3
    elif line_specification == 'c3' :
        g_code = move_arc_2(
            math.pi, 2*math.pi - short_circle_angle_takeback,
            machining_parameters
        )
                                                                            # d1
    elif line_specification == 'd1' :
        g_code = move_arc_2(
            0, math.pi, machining_parameters
        )
                                                                            # d2
    elif line_specification == 'd2' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # d3
    elif line_specification == 'd3' :
        g_code = move_arc_2(math.pi, 2*math.pi, machining_parameters)
                                                                            # d4
    elif line_specification == 'd4' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # d5
    elif line_specification == 'd5' :
        g_code = move_vertical(8, machining_parameters)
                                                                            # e1
    elif line_specification == 'e1' :
        g_code = move_horizontal(2.5, machining_parameters)
                                                                            # e2
    elif line_specification == 'e2' :
        g_code = move_vertical(1, machining_parameters)
                                                                            # e3
    elif line_specification == 'e3' :
        g_code = move_arc_2(0, math.pi, machining_parameters)
                                                                            # e4
    elif line_specification == 'e4' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # e5
    elif line_specification == 'e5' :
        g_code = move_arc_2(
            math.pi, 2*math.pi - short_circle_angle_takeback,
            machining_parameters
        )
                                                                            # f1
    elif line_specification == 'f1' :
        g_code = move_vertical(6.5, machining_parameters)
                                                                            # f2
    elif line_specification == 'f2' :
        g_code = move_quarter_arc(math.pi, math.pi/2, machining_parameters)
                                                                            # f3
    elif line_specification == 'f3' :
        if lift_for_drill_back :
            g_code = lift_drill(LIFT_UP, machining_parameters)
            g_code += move_quarter_arc(math.pi/2, math.pi, machining_parameters)
        else :
            g_code = move_quarter_arc(math.pi/2, math.pi, machining_parameters)
                                                                            # f4
    elif line_specification == 'f4' :
        if lift_for_drill_back :
            g_code = move_vertical(-1.5, machining_parameters)
            g_code += lift_drill(not LIFT_UP, machining_parameters)
        else :
            g_code = move_vertical(-1.5, machining_parameters)
                                                                            # f5
    elif line_specification == 'f5' :
        if lift_for_drill_back :
            g_code = move_horizontal(-1.5, machining_parameters)
            g_code += lift_drill(not LIFT_UP, machining_parameters)
        else :
            g_code = move_horizontal(-1.5, machining_parameters)
                                                                            # f6
    elif line_specification == 'f6' :
        g_code = move_horizontal(3, machining_parameters)
                                                                            # g1
    elif line_specification == 'g1' :
        g_code = move_arc_2(0, math.pi, machining_parameters)
                                                                            # g2
    elif line_specification == 'g2' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # g3
    elif line_specification == 'g3' :
        g_code = move_arc_2(math.pi, 2*math.pi, machining_parameters)
                                                                            # g4
    elif line_specification == 'g4' :
        g_code = move_back_vertical(
            3.5, machining_parameters, lift_for_drill_back
        )
                                                                            # g5
    elif line_specification == 'g5' :
        g_code = move_vertical(-6.5, machining_parameters)
                                                                            # g6
    elif line_specification == 'g6' :
        g_code = move_arc_2(
            2*math.pi, math.pi + short_circle_angle_takeback,
            machining_parameters
        )
                                                                            # h1
    elif line_specification == 'h1' :
        g_code = move_vertical(-8, machining_parameters)
                                                                            # h2
    elif line_specification == 'h2' :
        g_code = move_back_vertical(
            3.5, machining_parameters, lift_for_drill_back
        )
                                                                            # h3
    elif line_specification == 'h3' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # h4
    elif line_specification == 'h4' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # i1
    elif line_specification == 'i1' :
        g_code = move_vertical(5, machining_parameters)
                                                                            # i2
    elif line_specification == 'i2' :
        temp_machining_parameters = machining_parameters.copy()
        temp_machining_parameters['pass_depth'] = \
            2*machining_parameters['pass_depth']
        g_code = lift_drill(LIFT_UP, temp_machining_parameters)
        g_code += gcode_lib.move_fast(0, 2*drill_diameter, 0, move_speed)
        g_code += lift_drill(not LIFT_UP, temp_machining_parameters)
                                                                            # j1
    elif line_specification == 'j1' :
        g_code = move_arc_2(1.5*math.pi, 2*math.pi, machining_parameters)
                                                                            # j2
    elif line_specification == 'j2' :
        g_code = move_vertical(6.5, machining_parameters)
                                                                            # j3
    elif line_specification == 'j3' :
        g_code = gcode_lib.move_steady(0, 0, 2*pass_depth, bore_speed)
        g_code += gcode_lib.move_fast(0, 2*drill_diameter, 0, move_speed)
        g_code += gcode_lib.move_steady(0, 0, -2*pass_depth, bore_speed)
                                                                            # k1
    elif line_specification == 'k1' :
        g_code = move_vertical(-8, machining_parameters)
                                                                            # k2
    elif line_specification == 'k2' :
        g_code = move_back_vertical(
            2, machining_parameters, lift_for_drill_back
        )
                                                                            # k3
    elif line_specification == 'k3' :
        g_code = gcode_lib.move_steady(
            3*drill_diameter, 3*drill_diameter, 0, drill_speed
        )
                                                                            # k4
    elif line_specification == 'k4' :
        g_code = gcode_lib.move_steady(
            -2*drill_diameter, -2*drill_diameter, 0, drill_speed
        )
                                                                            # k5
    elif line_specification == 'k5' :
        g_code = gcode_lib.move_steady(
            2*drill_diameter, -3*drill_diameter, 0, drill_speed
        )
                                                                            # l1
    elif line_specification == 'l1' :
        g_code = move_vertical(-6.5, machining_parameters)
                                                                            # l2
    elif line_specification == 'l2' :
        g_code = move_quarter_arc(math.pi, 1.5*math.pi, machining_parameters)
                                                                            # m1
    elif line_specification == 'm1' :
        g_code = move_vertical(5, machining_parameters)
                                                                            # m2
    elif line_specification == 'm2' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # m3
    elif line_specification == 'm3' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # m4
    elif line_specification == 'm4' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # m5
    elif line_specification == 'm5' :
        g_code = move_back_vertical(
            3.5, machining_parameters, lift_for_drill_back
        )
                                                                            # m6
    elif line_specification == 'm6' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # m7
    elif line_specification == 'm7' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # n1
    elif line_specification == 'n1' :
        g_code = move_vertical(5, machining_parameters)
                                                                            # n2
    elif line_specification == 'n2' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # n3
    elif line_specification == 'n3' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # n4
    elif line_specification == 'n4' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # o1
    elif line_specification == 'o1' :
        g_code = move_vertical(2, machining_parameters)
                                                                            # o2
    elif line_specification == 'o2' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # o3
    elif line_specification == 'o3' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # o4
    elif line_specification == 'o4' :
        g_code = move_arc_2(2*math.pi, math.pi, machining_parameters)
                                                                            # p1
    elif line_specification == 'p1' :
        g_code = move_vertical(8, machining_parameters)
                                                                            # p2
    elif line_specification == 'p2' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # p3
    elif line_specification == 'p3' :
        g_code = move_arc_2(math.pi, 0, machining_parameters)
                                                                            # p4
    elif line_specification == 'p4' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # p5
    elif line_specification == 'p5' :
        g_code = move_arc_2(2*math.pi, math.pi, machining_parameters)
                                                                            # q1
    elif line_specification == 'q1' :
        g_code = move_arc_2(0, math.pi, machining_parameters)
                                                                            # q2
    elif line_specification == 'q2' :
        g_code = move_vertical(-2, machining_parameters)
                                                                            # q3
    elif line_specification == 'q3' :
        g_code = move_arc_2(math.pi, 2*math.pi, machining_parameters)
                                                                            # q4
    elif line_specification == 'q4' :
        g_code = move_back_vertical(
            3.5, machining_parameters, lift_for_drill_back
        )
                                                                            # q5
    elif line_specification == 'q5' :
        g_code = move_vertical(-8, machining_parameters)
                                                                            # r1
    elif line_specification == 'r1' :
        g_code = move_vertical(5, machining_parameters)
                                                                            # r2
    elif line_specification == 'r2' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # r3
    elif line_specification == 'r3' :
        g_code = move_quarter_arc(math.pi, math.pi/2, machining_parameters)
                                                                            # r4
    elif line_specification == 'r4' :
        g_code = move_horizontal(0.5, machining_parameters)
                                                                            # s1
    elif line_specification == 's1' :
        g_code = move_arc_2(
            short_circle_angle_takeback, math.pi, machining_parameters
        )
                                                                            # s2
    elif line_specification == 's2' :
        g_code = move_small_quarter_arc(
            math.pi, 1.5*math.pi, machining_parameters
        )
                                                                            # s3
    elif line_specification == 's3' :
        g_code = move_horizontal(1, machining_parameters)
                                                                            # s4
    elif line_specification == 's4' :
        g_code = move_small_quarter_arc(math.pi/2, 0, machining_parameters)
                                                                            # s5
    elif line_specification == 's5' :
        g_code = move_arc_2(
            2*math.pi, math.pi + short_circle_angle_takeback,
            machining_parameters
        )
                                                                            # t1
    elif line_specification == 't1' :
        g_code = move_horizontal(2, machining_parameters)
                                                                            # t2
    elif line_specification == 't2' :
        if lift_for_drill_back :
            g_code = lift_drill(LIFT_UP, machining_parameters)
            g_code += move_horizontal(-1, machining_parameters)
        else :
            g_code = move_horizontal(-1, machining_parameters)
                                                                            # t3
    elif line_specification == 't3' :
        if lift_for_drill_back :
            g_code = move_vertical(3, machining_parameters)
            g_code += lift_drill(not LIFT_UP, machining_parameters)
        else :
            g_code = move_vertical(3, machining_parameters)
                                                                            # t4
    elif line_specification == 't4' :
        g_code = move_vertical(-6.5, machining_parameters)
                                                                            # t5
    elif line_specification == 't5' :
        g_code = move_quarter_arc(math.pi, 1.5*math.pi, machining_parameters)
                                                                            # u1
    elif line_specification == 'u1' :
        g_code = move_vertical(-3.5, machining_parameters)
                                                                            # u2
    elif line_specification == 'u2' :
        g_code = move_arc_2(math.pi, 2*math.pi, machining_parameters)
                                                                            # u3
    elif line_specification == 'u3' :
        g_code = move_back_vertical(
            -1.5, machining_parameters, lift_for_drill_back
        )
                                                                            # u4
    elif line_specification == 'u4' :
        g_code = move_vertical(5, machining_parameters)
                                                                            # v1
    elif line_specification == 'v1' :
        g_code = move_diagonal(1.5, -5, machining_parameters)
                                                                            # v2
    elif line_specification == 'v2' :
        g_code = move_diagonal(1.5, 5, machining_parameters)
                                                                            # w1
    elif line_specification == 'w1' :
        g_code = move_diagonal(1.5, -5, machining_parameters)
                                                                            # w2
    elif line_specification == 'w2' :
        g_code = move_diagonal(1.5, 5, machining_parameters)
                                                                            # w3
    elif line_specification == 'w3' :
        g_code = move_diagonal(1.5, -5, machining_parameters)
                                                                            # w4
    elif line_specification == 'w4' :
        g_code = move_diagonal(1.5, 5, machining_parameters)
                                                                            # x1
    elif line_specification == 'x1' :
        g_code = move_diagonal(3, 5, machining_parameters)
                                                                            # x2
    elif line_specification == 'x2' :
        g_code = move_back_diagonal(
            -1.5, -2.5, machining_parameters, lift_for_drill_back
        )
                                                                            # x3
    elif line_specification == 'x3' :
        g_code = move_back_diagonal(
            -1.5, 2.5, machining_parameters, lift_for_drill_back
        )
                                                                            # x4
    elif line_specification == 'x4' :
        g_code = move_diagonal(3, -5, machining_parameters)
                                                                            # y1
    elif line_specification == 'y1' :
        g_code = move_diagonal(1.5, -5, machining_parameters)
                                                                            # y2
    elif line_specification == 'y2' :
        g_code = move_back_diagonal(
            1.5, 5, machining_parameters, lift_for_drill_back
        )
                                                                            # y3
    elif line_specification == 'y3' :
        g_code = move_diagonal(-8/5*1.5, -8, machining_parameters)
                                                                            # z1
    elif line_specification == 'z1' :
        g_code = move_horizontal(3, machining_parameters)
                                                                            # z2
    elif line_specification == 'z2' :
        g_code = move_diagonal(-3, -5, machining_parameters)
                                                                            # z3
    elif line_specification == 'z3' :
        g_code = move_horizontal(3, machining_parameters)
        
    # ..........................................................................
                                                                            # A1
    elif line_specification == 'A1' :
        g_code = move_diagonal(
            uc_letter_width/2, uc_letter_height, machining_parameters
        )
                                                                            # A2
    elif line_specification == 'A2' :
        g_code = move_diagonal(
            uc_letter_width/2, -uc_letter_height, machining_parameters
        )
                                                                            # A3
    elif line_specification == 'A3' :
        g_code = move_back_diagonal(
            -1*uc_letter_width/uc_letter_height, 2,
            machining_parameters, lift_for_drill_back
        )
                                                                            # A4
    elif line_specification == 'A4' :
        g_code = move_horizontal(
            -uc_letter_width + 2*uc_letter_width/uc_letter_height,
            machining_parameters
        )
                                                                            # B1
    elif line_specification == 'B1' :
        g_code = move_horizontal(
            uc_letter_width - uc_circle_radius, machining_parameters
        )
                                                                            # B2
    elif line_specification == 'B2' :
        g_code = move_arc_2(
            -math.pi/2, math.pi/2,
            machining_parameters, uc_circle_radius
        )
                                                                            # B3
    elif line_specification == 'B3' :
        g_code = move_horizontal(
            -(uc_letter_width - uc_circle_radius), machining_parameters
        )
                                                                            # B4
    elif line_specification == 'B4' :
        g_code = move_vertical(
            -uc_letter_height,
            machining_parameters
        )
                                                                            # B5
    elif line_specification == 'B5' :
        g_code = move_horizontal(
            uc_letter_width - uc_circle_radius, machining_parameters
        )
                                                                            # B6
    elif line_specification == 'B6' :
        g_code = move_arc_2(
            -math.pi/2, math.pi/2,
            machining_parameters, uc_circle_radius
        )

    return(g_code)

# ..............................................................................
                                                   # line set for each character
def build_line_set(character) :
    line_set = []
    entry_point = [0, 0]
    exit_point  = [0, 0]
                                                                             # a
    if character == 'a' :
        line_set    = ['a1', 'a2', 'a3', 'a4', 'a5', 'a6']
        entry_point = [
            short_circle_final_x_offset,
            3.5 + short_circle_final_y_offset
        ]
        exit_point  = [-0.5, 2.5]
                                                                             # b
    elif character == 'b' :
        line_set    = ['b1', 'b2', 'b3', 'b4', 'b5']
        entry_point = [0, 0]
        exit_point  = [-2*lc_circle_radius, lc_circle_radius]
                                                                             # c
    elif character == 'c' :
        line_set    = ['c1', 'c2', 'c3']
        entry_point = [
            lc_letter_width - short_circle_final_x_offset,
            3.5 + short_circle_final_y_offset
        ]
        exit_point  = [
            -short_circle_final_x_offset,
            lc_circle_radius - short_circle_final_y_offset
        ]
                                                                             # d
    elif character == 'd' :
        line_set    = ['d1', 'd2', 'd3', 'd4', 'd5']
        entry_point = [lc_letter_width, 3.5]
        exit_point  = [0, 8]
                                                                             # e
    elif character == 'e' :
        line_set    = ['e1', 'e2', 'e3', 'e4', 'e5']
        entry_point = [0.5, 2.5]
        exit_point  = [
            -short_circle_final_x_offset,
            lc_circle_radius - short_circle_final_y_offset
        ]
                                                                             # f
    elif character == 'f' :
        line_set    = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
        entry_point = [0, 0]
        exit_point  = [0, lc_letter_height]
                                                                             # g
    elif character == 'g' :
        line_set    = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6']
        entry_point = [lc_letter_width, 3.5]
        exit_point  = [
            -2*lc_circle_radius + short_circle_final_x_offset,
            -1.5 - short_circle_final_y_offset
        ]
                                                                             # h
    elif character == 'h' :
        line_set    = ['h1', 'h2', 'h3', 'h4']
        entry_point = [0, 8]
        exit_point  = [0, 0]
                                                                             # i
    elif character == 'i' :
        line_set    = ['i1', 'i2']
        entry_point = [0, 0]
        exit_point  = [0, 7]
                                                                             # j
    elif character == 'j' :
        line_set    = ['j1', 'j2', 'j3']
        entry_point = [0, -3]
        exit_point  = [0, 7]
                                                                             # k
    elif character == 'k' :
        line_set    = ['k1', 'k2', 'k3', 'k4', 'k5']
        entry_point = [0, 8]
        exit_point  = [0, 0]
                                                                             # l
    elif character == 'l' :
        line_set    = ['l1', 'l2']
        entry_point = [0, 8]
        exit_point  = [0, 0]
                                                                             # m
    elif character == 'm' :
        line_set    = ['m1', 'm2', 'm3', 'm4', 'm5', 'm6', 'm7']
        entry_point = [0, 0]
        exit_point  = [0, 0]
                                                                             # n
    elif character == 'n' :
        line_set    = ['n1', 'n2', 'n3', 'n4']
        entry_point = [0, 0]
        exit_point  = [0, 0]
                                                                             # o
    elif character == 'o' :
        line_set    = ['o1', 'o2', 'o3', 'o4']
        entry_point = [0, 1.5]
        exit_point  = [-lc_letter_width, lc_circle_radius]
                                                                             # p
    elif character == 'p' :
        line_set    = ['p1', 'p2', 'p3', 'p4', 'p5']
        entry_point = [0, -3]
        exit_point  = [-lc_letter_width, lc_circle_radius]
                                                                             # q
    elif character == 'q' :
        line_set    = ['q1', 'q2', 'q3', 'q4', 'q5']
        entry_point = [lc_letter_width, 3.5]
        exit_point  = [0, -3]
                                                                             # r
    elif character == 'r' :
        line_set    = ['r1', 'r2', 'r3', 'r4']
        entry_point = [0, 0]
        exit_point  = [0, lc_letter_height]
                                                                             # s
    elif character == 's' :
        line_set    = ['s1', 's2', 's3', 's4', 's5']
        entry_point = [
            lc_letter_width - short_circle_final_x_offset,
            3.5 + short_circle_final_y_offset
        ]
        exit_point  = [
            -lc_letter_width + short_circle_final_x_offset,
            lc_circle_radius - short_circle_final_y_offset
        ]
                                                                             # t
    elif character == 't' :
        line_set    = ['t1', 't2', 't3', 't4', 't5']
        entry_point = [0, lc_letter_height]
        exit_point  = [0, 0]
                                                                             # u
    elif character == 'u' :
        line_set    = ['u1', 'u2', 'u3', 'u4']
        entry_point = [0, lc_letter_height]
        exit_point  = [0, lc_letter_height]
                                                                             # v
    elif character == 'v' :
        line_set    = 'm 0 5 l 1.5 -5 l 1.5 5'
                                                                             # w
    elif character == 'w' :
        line_set    = 'm 0 5 l 1.5 -5 l 1.5 5 l 1.5 -5 l 1.5 5'
                                                                             # x
    elif character == 'x' :
        line_set    = 'l 3 5 m -1.5 -2.5 m -1.5 2.5 l 3 -5'
                                                                             # y
    elif character == 'y' :
        line_set    = 'm 0 5 l 1.5 -5 m 1.5 5 l -2.4 -8'
                                                                             # z
    elif character == 'z' :
        line_set    = 'm 0 5 h 3 l -3 -5 h 3'

    # ..........................................................................
                                                                             # A
    elif character == 'A' :
        line_set    = 'l 2 8 l 2 -8 m -0.5 2 h -3'
                                                                             # B
    elif character == 'B' :
        line_set    = 'm 0 4 h 2 a 2 -90 90 h -2 v -8 h 2 a 2 -90 90'
                                                                             # C
    elif character == 'C' :
        line_set    = 'm 4 6 a 2 0 180 v -4 a 2 180 360'
                                                                             # D
    elif character == 'D' :
        line_set    = 'v 8 h 2 a 2 90 0 v -4 a 2 0 -90 h -2'
                                                                             # E
    elif character == 'E' :
        line_set    = 'm 4 8 h -4 v -8 h 4 m -4 0 m 0 4 h 3'
                                                                             # F
    elif character == 'F' :
        line_set    = 'm 4 8 h -4 v -8 m 0 4 h 3'
                                                                             # G
    elif character == 'G' :
        line_set    = 'm 2 3.5 h 2 v -1.5 a 2 360 180 v 4 a 2 180 0'
                                                                             # H
    elif character == 'H' :
        line_set    = 'v 8 m 0 -4 h 4 m 0 4 v -8'
                                                                             # I
    elif character == 'I' :
        line_set    = 'v 8'
                                                                             # J
    elif character == 'J' :
        line_set    = 'a 2 -90 0 v 6'
                                                                             # K
    elif character == 'K' :
        line_set    = 'm 0 8 v -8 m 0 2 l 4 6 m -2.75 -4.5 l 2.75 -3.5'
                                                                             # L
    elif character == 'L' :
        line_set    = 'm 0 8 v -8 h 4'
                                                                             # N
    elif character == 'N' :
        line_set    = 'v 8 l 4 -8 v 8'
                                                                             # M
    elif character == 'M' :
        line_set    = 'v 8 l 2.5 -4 l 2.5 4 v -8'
                                                                             # O
    elif character == 'O' :
        line_set    = 'm 0 2 a 2 180 360 v 4 a 2 0 180 v -4'
                                                                             # P
    elif character == 'P' :
        line_set    = 'v 8 h 2 a 2 90 -90 h -2'
                                                                             # Q
    elif character == 'Q' :
        line_set    = 'm 3 2 l 2 -2 m -1 1 v 5 a 2 0 180 v -4 a 2 -180 -45'
                                                                             # R
    elif character == 'R' :
        line_set    = 'v 8 h 2 a 2 90 -90 h -2 m 2 0 l 2 -4'
                                                                             # S
    elif character == 'S' :
        line_set    = 'm 0 2 a 2 -180 90 a 2 270 0'
                                                                             # T
    elif character == 'T' :
        line_set    = 'm 0 8 h 4 m -2 0 v -8'
                                                                             # U
    elif character == 'U' :
        line_set    = 'm 0 8 v -6 a 2 180 360 v6'
                                                                             # V
    elif character == 'V' :
        line_set    = 'm 0 8 l 2 -8 l 2 8'
                                                                             # W
    elif character == 'W' :
        line_set    = 'm 0 8 l 2 -8 l 2 8 l 2 -8 l 2 8'
                                                                             # X
    elif character == 'X' :
        line_set    = 'l 4 8 m -2 -4 m -2 4 l 4 -8'
                                                                             # Y
    elif character == 'Y' :
        line_set    = 'm 0 8 l 2 -4 l 2 4 m -2 -4 v -4'
                                                                             # Z
    elif character == 'Z' :
        line_set    = 'm 0 8 h 4 l -4 -8 h 4'

    return(line_set, entry_point, exit_point)

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
    character,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
    pass_depth = machining_parameters['pass_depth']
    bore_speed = machining_parameters['drill_bore_speed']
                                                                       # comment
    g_code = "; %s\n" % character
                                                                     # dive down
    g_code += gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
                                                                   # drill lines
    (line_set, entry_point, exit_point) = build_line_set(character)
    if type(line_set) is str :
        (character_g_code, entry_point, exit_point) = line_set_to_gcode(
            line_set, machining_parameters, lift_for_drill_back
        )
        if character == 'K' :
            print(character + ' :')
            print(character_g_code)
            print('entry : ' + repr(entry_point))
            print('exit : ' + repr(exit_point))
        g_code += character_g_code
    else :
        for line in line_set :
            g_code += build_line_g_code(
                line,
                letter_machining_parameters,
                lift_for_drill_back
            )
                                                                  # dive back up
    g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)

    return(g_code, entry_point, exit_point)

# ------------------------------------------------------------------------------
def line_g_code(
    line,
    machining_parameters=letter_machining_parameters,
    lift_for_drill_back=False
) :
                                                             # write line g-code
    drill_tool_diameter = machining_parameters['drill_diameter']
    text_g_code = gcode_lib.select_tool(drill_tool_diameter)
                                                              # drill characters
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
                character,
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
