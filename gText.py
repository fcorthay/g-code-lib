#!/usr/bin/python3
import os
import math
import gcode_lib

# ------------------------------------------------------------------------------
                                                                   # test string
test_string = 'the quick brown fox jumps over the lazy dog'

# ------------------------------------------------------------------------------
                                                             # letter parameters
drill_diameter = 2
letter_spacing = 2
space_spacing = 4

letter_width = 3
letter_height = 5
usual_circle_radius = letter_width/2
small_circle_radius = letter_width/3

# ------------------------------------------------------------------------------
                                                           # drilling parameters
letter_machining_parameters = gcode_lib.default_machining_parameters
letter_machining_parameters[gcode_lib.drill_diameter_id] = drill_diameter
letter_displacement_speeds = gcode_lib.default_displacement_speeds

pass_depth = letter_machining_parameters[gcode_lib.pass_depth_id]
move_speed = letter_displacement_speeds[gcode_lib.fast_displacement_speed_id]
drill_speed = letter_displacement_speeds[gcode_lib.drill_displacement_speed_id]
bore_speed = letter_displacement_speeds[gcode_lib.drill_bore_speed_id]

half_circle_facet_nb = 8
quarter_circle_facet_nb = round(half_circle_facet_nb/2)
short_circle_final_y_offset = 1/2
short_circle_angle_takeback = math.atan2(
    short_circle_final_y_offset, usual_circle_radius
)
short_circle_final_x_offset = \
    usual_circle_radius*(1 - math.cos(short_circle_angle_takeback))

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
                                                               # horizontal line
def move_horizontal(
    displacement, drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = gcode_lib.move_steady(
        displacement*drill_diameter, 0, 0, drill_speed
    )

    return (g_code)

# ..............................................................................
                                                                 # vertical line
def move_vertical(
    displacement, drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = gcode_lib.move_steady(
        0, displacement*drill_diameter, 0, drill_speed
    )

    return (g_code)

# ..............................................................................
                                                                 # vertical line
def move_diagonal(
    x_displacement, y_displacement,
    drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = gcode_lib.move_steady(
        x_displacement*drill_diameter, y_displacement*drill_diameter,
        0, drill_speed
    )

    return (g_code)

# ..............................................................................
                                                            # vertical move back
def move_back_vertical(
    y_displacement,
    lift_for_drill_back=lift_for_drill_back,
    z_displacement=pass_depth,
    drill_diameter=drill_diameter,
    move_speed=move_speed, drill_speed=drill_speed, bore_speed=bore_speed
) :
    if lift_for_drill_back :
        g_code = gcode_lib.move_steady(0, 0, z_displacement, bore_speed)
        g_code += gcode_lib.move_fast(
            0, y_displacement*drill_diameter, 0, move_speed
        )
        g_code += gcode_lib.move_steady(0, 0, -z_displacement, bore_speed)
    else :
        g_code = gcode_lib.move_steady(
            0, y_displacement*drill_diameter, 0, drill_speed
        )

    return (g_code)

# ..............................................................................
                                                            # diagonal move back
def move_back_diagonal(
    x_displacement, y_displacement,
    lift_for_drill_back=lift_for_drill_back,
    z_displacement=pass_depth,
    drill_diameter=drill_diameter,
    move_speed=move_speed, drill_speed=drill_speed, bore_speed=bore_speed
) :
    if lift_for_drill_back :
        g_code = gcode_lib.move_steady(0, 0, z_displacement, bore_speed)
        g_code += gcode_lib.move_fast(
            x_displacement*drill_diameter, y_displacement*drill_diameter,
            0, move_speed
        )
        g_code += gcode_lib.move_steady(0, 0, -z_displacement, bore_speed)
    else :
        g_code = gcode_lib.move_steady(
            x_displacement*drill_diameter, y_displacement*drill_diameter,
            0, drill_speed
        )

    return (g_code)

# ..............................................................................
                                                                # usual size arc
def move_arc(
    start_angle, end_angle,
    radius=usual_circle_radius,
    facet_nb=half_circle_facet_nb,
    drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = gcode_lib.circle_arc_gcode(
        radius*drill_diameter, facet_nb,
        start_angle, end_angle,
        drill_speed
    )

    return (g_code)

# ..............................................................................
                                                            # quarter circle arc
def move_quarter_arc(
    start_angle, end_angle,
    radius=usual_circle_radius,
    facet_nb=quarter_circle_facet_nb,
    drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = move_arc(
        start_angle, end_angle,
        radius, facet_nb,
        drill_diameter, drill_speed
    )

    return (g_code)

# ..............................................................................
                                                            # quarter circle arc
def move_quarter_arc(
    start_angle, end_angle,
    radius=usual_circle_radius,
    facet_nb=quarter_circle_facet_nb,
    drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = move_arc(
        start_angle, end_angle,
        radius, facet_nb,
        drill_diameter, drill_speed
    )

    return (g_code)

# ..............................................................................
                                                 # quarter of a small circle arc
def move_small_quarter_arc(
    start_angle, end_angle,
    radius=small_circle_radius,
    facet_nb=quarter_circle_facet_nb,
    drill_diameter=drill_diameter, drill_speed=drill_speed
) :
    g_code = move_arc(
        start_angle, end_angle,
        radius, facet_nb,
        drill_diameter, drill_speed
    )

    return (g_code)

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
                                                                            # a1
    if line_specification == 'a1' :
        g_code = move_arc(math.pi - short_circle_angle_takeback, 0)
                                                                            # a2
    elif line_specification == 'a2' :
        g_code = move_vertical(-3.5)
                                                                            # a3
    elif line_specification == 'a3' :
        g_code = move_back_vertical(1.5)
                                                                            # a4
    elif line_specification == 'a4' :
        g_code = move_arc(2*math.pi, math.pi)
                                                                            # a5
    elif line_specification == 'a5' :
        g_code = move_small_quarter_arc(math.pi, math.pi/2)
                                                                            # a6
    elif line_specification == 'a6' :
        g_code = move_horizontal(2)
                                                                            # b1
    elif line_specification == 'b1' :
        g_code = move_vertical(8)
                                                                            # b2
    elif line_specification == 'b2' :
        g_code = move_back_vertical(-4.5)
                                                                            # b3
    elif line_specification == 'b3' :
        g_code = move_arc(math.pi, 0)
                                                                            # b4
    elif line_specification == 'b4' :
        g_code = move_vertical(-2)
                                                                            # b5
    elif line_specification == 'b5' :
        g_code = move_arc(2*math.pi, math.pi)
                                                                            # c1
    elif line_specification == 'c1' :
        g_code = move_arc(short_circle_angle_takeback, math.pi)
                                                                            # c2
    elif line_specification == 'c2' :
        g_code = move_vertical(-2)
                                                                            # c3
    elif line_specification == 'c3' :
        g_code = move_arc(math.pi, 2*math.pi - short_circle_angle_takeback)
                                                                            # d1
    elif line_specification == 'd1' :
        g_code = gcode_lib.circle_arc_gcode(
            usual_circle_radius*drill_diameter, half_circle_facet_nb,
            0, math.pi,
            drill_speed
        )
                                                                            # d2
    elif line_specification == 'd2' :
        g_code = move_vertical(-2)
                                                                            # d3
    elif line_specification == 'd3' :
        g_code = move_arc(math.pi, 2*math.pi)
                                                                            # d4
    elif line_specification == 'd4' :
        g_code = move_back_vertical(-1.5)
                                                                            # d5
    elif line_specification == 'd5' :
        g_code = move_vertical(8)
                                                                            # e1
    elif line_specification == 'e1' :
        g_code = move_horizontal(2.5)
                                                                            # e2
    elif line_specification == 'e2' :
        g_code = move_vertical(1)
                                                                            # e3
    elif line_specification == 'e3' :
        g_code = move_arc(0, math.pi)
                                                                            # e4
    elif line_specification == 'e4' :
        g_code = move_vertical(-2)
                                                                            # e5
    elif line_specification == 'e5' :
        g_code = move_arc(math.pi, 2*math.pi - short_circle_angle_takeback)
                                                                            # f1
    elif line_specification == 'f1' :
        g_code = move_vertical(6.5)
                                                                            # f2
    elif line_specification == 'f2' :
        g_code = move_quarter_arc(math.pi, math.pi/2)
                                                                            # f3
    elif line_specification == 'f3' :
        if lift_for_drill_back :
            g_code = gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
            g_code += move_quarter_arc(math.pi/2, math.pi)
        else :
            g_code = move_quarter_arc(math.pi/2, math.pi)
                                                                            # f4
    elif line_specification == 'f4' :
        if lift_for_drill_back :
            g_code += gcode_lib.move_fast(0, -1.5*drill_diameter, 0, move_speed)
        else :
            g_code = move_vertical(-1.5)
                                                                            # f5
    elif line_specification == 'f5' :
        if lift_for_drill_back :
            g_code += gcode_lib.move_fast(-1.5*drill_diameter, 0, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
        else :
            g_code = move_horizontal(-1.5)
                                                                            # f6
    elif line_specification == 'f6' :
        g_code = move_horizontal(3)
                                                                            # g1
    elif line_specification == 'g1' :
        g_code = move_arc(0, math.pi)
                                                                            # g2
    elif line_specification == 'g2' :
        g_code = move_vertical(-2)
                                                                            # g3
    elif line_specification == 'g3' :
        g_code = move_arc(math.pi, 2*math.pi)
                                                                            # g4
    elif line_specification == 'g4' :
        g_code = move_back_vertical(3.5)
                                                                            # g5
    elif line_specification == 'g5' :
        g_code = move_vertical(-6.5)
                                                                            # g6
    elif line_specification == 'g6' :
        g_code = move_arc(2*math.pi, math.pi + short_circle_angle_takeback)
                                                                            # h1
    elif line_specification == 'h1' :
        g_code = move_vertical(-8)
                                                                            # h2
    elif line_specification == 'h2' :
        g_code = move_back_vertical(3.5)
                                                                            # h3
    elif line_specification == 'h3' :
        g_code = move_arc(math.pi, 0)
                                                                            # h4
    elif line_specification == 'h4' :
        g_code = move_vertical(-3.5)
                                                                            # i1
    elif line_specification == 'i1' :
        g_code = move_vertical(5)
                                                                            # i2
    elif line_specification == 'i2' :
        g_code = gcode_lib.move_steady(0, 0, 2*pass_depth, bore_speed)
        g_code += gcode_lib.move_fast(0, 2*drill_diameter, 0, move_speed)
        g_code += gcode_lib.move_steady(0, 0, -2*pass_depth, bore_speed)
                                                                            # j1
    elif line_specification == 'j1' :
        g_code = move_arc(1.5*math.pi, 2*math.pi)
                                                                            # j2
    elif line_specification == 'j2' :
        g_code = move_vertical(6.5)
                                                                            # j3
    elif line_specification == 'j3' :
        g_code = gcode_lib.move_steady(0, 0, 2*pass_depth, bore_speed)
        g_code += gcode_lib.move_fast(0, 2*drill_diameter, 0, move_speed)
        g_code += gcode_lib.move_steady(0, 0, -2*pass_depth, bore_speed)
                                                                            # k1
    elif line_specification == 'k1' :
        g_code = move_vertical(-8)
                                                                            # k2
    elif line_specification == 'k2' :
        g_code = move_back_vertical(2)
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
        g_code = move_vertical(-6.5)
                                                                            # l2
    elif line_specification == 'l2' :
        g_code = move_quarter_arc(math.pi, 1.5*math.pi)
                                                                            # m1
    elif line_specification == 'm1' :
        g_code = move_vertical(5)
                                                                            # m2
    elif line_specification == 'm2' :
        g_code = move_back_vertical(-1.5)
                                                                            # m3
    elif line_specification == 'm3' :
        g_code = move_arc(math.pi, 0)
                                                                            # m4
    elif line_specification == 'm4' :
        g_code = move_vertical(-3.5)
                                                                            # m5
    elif line_specification == 'm5' :
        g_code = move_back_vertical(3.5)
                                                                            # m6
    elif line_specification == 'm6' :
        g_code = move_arc(math.pi, 0)
                                                                            # m7
    elif line_specification == 'm7' :
        g_code = move_vertical(-3.5)
                                                                            # n1
    elif line_specification == 'n1' :
        g_code = move_vertical(5)
                                                                            # n2
    elif line_specification == 'n2' :
        g_code = move_back_vertical(-1.5)
                                                                            # n3
    elif line_specification == 'n3' :
        g_code = move_arc(math.pi, 0)
                                                                            # n4
    elif line_specification == 'n4' :
        g_code = move_vertical(-3.5)
                                                                            # o1
    elif line_specification == 'o1' :
        g_code = move_vertical(2)
                                                                            # o2
    elif line_specification == 'o2' :
        g_code = move_arc(math.pi, 0)
                                                                            # o3
    elif line_specification == 'o3' :
        g_code = move_vertical(-2)
                                                                            # o4
    elif line_specification == 'o4' :
        g_code = move_arc(2*math.pi, math.pi)
                                                                            # p1
    elif line_specification == 'p1' :
        g_code = move_vertical(8)
                                                                            # p2
    elif line_specification == 'p2' :
        g_code = move_back_vertical(-1.5)
                                                                            # p3
    elif line_specification == 'p3' :
        g_code = move_arc(math.pi, 0)
                                                                            # p4
    elif line_specification == 'p4' :
        g_code = move_vertical(-2)
                                                                            # p5
    elif line_specification == 'p5' :
        g_code = move_arc(2*math.pi, math.pi)
                                                                            # q1
    elif line_specification == 'q1' :
        g_code = move_arc(0, math.pi)
                                                                            # q2
    elif line_specification == 'q2' :
        g_code = move_vertical(-2)
                                                                            # q3
    elif line_specification == 'q3' :
        g_code = move_arc(math.pi, 2*math.pi)
                                                                            # q4
    elif line_specification == 'q4' :
        g_code = move_back_vertical(3.5)
                                                                            # q5
    elif line_specification == 'q5' :
        g_code = move_vertical(-8)
                                                                            # r1
    elif line_specification == 'r1' :
        g_code = move_vertical(5)
                                                                            # r2
    elif line_specification == 'r2' :
        g_code = move_back_vertical(-1.5)
                                                                            # r3
    elif line_specification == 'r3' :
        g_code = move_quarter_arc(math.pi, math.pi/2)
                                                                            # r4
    elif line_specification == 'r4' :
        g_code = move_horizontal(0.5)
                                                                            # s1
    elif line_specification == 's1' :
        g_code = move_arc(short_circle_angle_takeback, math.pi)
                                                                            # s2
    elif line_specification == 's2' :
        g_code = move_small_quarter_arc(math.pi, 1.5*math.pi)
                                                                            # s3
    elif line_specification == 's3' :
        g_code = move_horizontal(1)
                                                                            # s4
    elif line_specification == 's4' :
        g_code = move_small_quarter_arc(math.pi/2, 0)
                                                                            # s5
    elif line_specification == 's5' :
        g_code = move_arc(2*math.pi, math.pi + short_circle_angle_takeback)
                                                                            # t1
    elif line_specification == 't1' :
        g_code = move_horizontal(2)
                                                                            # t2
    elif line_specification == 't2' :
        if lift_for_drill_back :
            g_code += gcode_lib.move_steady(0, 0, pass_depth, bore_speed)
            g_code += gcode_lib.move_fast(-1*drill_diameter, 0, 0, move_speed)
        else :
            g_code = gcode_lib.move_steady(-1*drill_diameter, 0, 0, drill_speed)
                                                                            # t3
    elif line_specification == 't3' :
        if lift_for_drill_back :
            g_code += gcode_lib.move_fast(0, 3*drill_diameter, 0, move_speed)
            g_code += gcode_lib.move_steady(0, 0, -pass_depth, bore_speed)
        else :
            g_code = gcode_lib.move_steady(0, 3*drill_diameter, 0, drill_speed)
                                                                            # t4
    elif line_specification == 't4' :
        g_code = move_vertical(-6.5)
                                                                            # t5
    elif line_specification == 't5' :
        g_code = move_quarter_arc(math.pi, 1.5*math.pi)
                                                                            # u1
    elif line_specification == 'u1' :
        g_code = move_vertical(-3.5)
                                                                            # u2
    elif line_specification == 'u2' :
        g_code = move_arc(math.pi, 2*math.pi)
                                                                            # u3
    elif line_specification == 'u3' :
        g_code = move_back_vertical(-1.5)
                                                                            # u4
    elif line_specification == 'u4' :
        g_code = move_vertical(5)
                                                                            # v1
    elif line_specification == 'v1' :
        g_code = move_diagonal(1.5, -5)                                                                # v1
                                                                            # v2
    elif line_specification == 'v2' :
        g_code = move_diagonal(1.5, 5)                                                                # v1
                                                                            # w1
    elif line_specification == 'w1' :
        g_code = move_diagonal(1.5, -5)                                                                # v1
                                                                            # w2
    elif line_specification == 'w2' :
        g_code = move_diagonal(1.5, 5)                                                                # v1
                                                                            # w3
    elif line_specification == 'w3' :
        g_code = move_diagonal(1.5, -5)                                                                # v1
                                                                            # w4
    elif line_specification == 'w4' :
        g_code = move_diagonal(1.5, 5)                                                                # v1
                                                                            # x1
    elif line_specification == 'x1' :
        g_code = move_diagonal(3, 5)                                                                # v1
                                                                            # x2
    elif line_specification == 'x2' :
        g_code = move_back_diagonal(-1.5, -2.5)                                                                # v1
                                                                            # x3
    elif line_specification == 'x3' :
        g_code = move_back_diagonal(-1.5, 2.5)                                                                # v1
                                                                            # x4
    elif line_specification == 'x4' :
        g_code = move_diagonal(3, -5)                                                                # v1
# ..............................................................................
                                                                            # y1
    elif line_specification == 'y1' :
        g_code = move_diagonal(1.5, -5)                                                                # v1
                                                                            # y2
    elif line_specification == 'y2' :
        g_code = move_back_diagonal(1.5, 5)                                                                # v1
                                                                            # y3
    elif line_specification == 'y3' :
        g_code = move_diagonal(-8/5*1.5, -8)                                                                # v1
# ..............................................................................
                                                                            # z1
    elif line_specification == 'z1' :
        g_code = move_horizontal(3)                                                                # v1
                                                                            # z2
    elif line_specification == 'z2' :
        g_code = move_diagonal(-3, -5)                                                                # v1
                                                                            # z3
    elif line_specification == 'z3' :
        g_code = move_horizontal(3)                                                                # v1

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
        exit_point  = [-2*usual_circle_radius, usual_circle_radius]
                                                                             # c
    elif character == 'c' :
        line_set    = ['c1', 'c2', 'c3']
        entry_point = [
            letter_width - short_circle_final_x_offset,
            3.5 + short_circle_final_y_offset
        ]
        exit_point  = [
            -short_circle_final_x_offset,
            usual_circle_radius - short_circle_final_y_offset
        ]
                                                                             # d
    elif character == 'd' :
        line_set    = ['d1', 'd2', 'd3', 'd4', 'd5']
        entry_point = [letter_width, 3.5]
        exit_point  = [0, 8]
                                                                             # e
    elif character == 'e' :
        line_set    = ['e1', 'e2', 'e3', 'e4', 'e5']
        entry_point = [0.5, 2.5]
        exit_point  = [
            -short_circle_final_x_offset,
            usual_circle_radius - short_circle_final_y_offset
        ]
                                                                             # f
    elif character == 'f' :
        line_set    = ['f1', 'f2', 'f3', 'f4', 'f5', 'f6']
        entry_point = [0, 0]
        exit_point  = [0, letter_height]
                                                                             # g
    elif character == 'g' :
        line_set    = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6']
        entry_point = [letter_width, 3.5]
        exit_point  = [
            -2*usual_circle_radius + short_circle_final_x_offset,
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
        exit_point  = [-letter_width, usual_circle_radius]
                                                                             # p
    elif character == 'p' :
        line_set    = ['p1', 'p2', 'p3', 'p4', 'p5']
        entry_point = [0, -3]
        exit_point  = [-letter_width, usual_circle_radius]
                                                                             # q
    elif character == 'q' :
        line_set    = ['q1', 'q2', 'q3', 'q4', 'q5']
        entry_point = [letter_width, 3.5]
        exit_point  = [0, -3]
                                                                             # r
    elif character == 'r' :
        line_set    = ['r1', 'r2', 'r3', 'r4']
        entry_point = [0, 0]
        exit_point  = [0, letter_height]
                                                                             # s
    elif character == 's' :
        line_set    = ['s1', 's2', 's3', 's4', 's5']
        entry_point = [
            letter_width - short_circle_final_x_offset,
            3.5 + short_circle_final_y_offset
        ]
        exit_point  = [
            -letter_width + short_circle_final_x_offset,
            usual_circle_radius - short_circle_final_y_offset
        ]
                                                                             # t
    elif character == 't' :
        line_set    = ['t1', 't2', 't3', 't4', 't5']
        entry_point = [0, letter_height]
        exit_point  = [0, 0]
                                                                             # u
    elif character == 'u' :
        line_set    = ['u1', 'u2', 'u3', 'u4']
        entry_point = [0, letter_height]
        exit_point  = [0, letter_height]
                                                                             # v
    elif character == 'v' :
        line_set    = ['v1', 'v2']
        entry_point = [0, letter_height]
        exit_point  = [0, letter_height]
                                                                             # w
    elif character == 'w' :
        line_set    = ['w1', 'w2', 'w3', 'w4']
        entry_point = [0, letter_height]
        exit_point  = [0, letter_height]
                                                                             # x
    elif character == 'x' :
        line_set    = ['x1', 'x2', 'x3', 'x4']
        entry_point = [0, 0]
        exit_point  = [0, 0]
                                                                             # y
    elif character == 'y' :
        line_set    = ['y1', 'y2', 'y3']
        entry_point = [0, letter_height]
        exit_point  = [-8/5*1.5, -3]
                                                                             # z
    elif character == 'z' :
        line_set    = ['z1', 'z2', 'z3']
        entry_point = [0, letter_height]
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
old_exit_point = [letter_spacing, 0]
for character in test_string :
    if character == ' ' :
        old_exit_point[0] = old_exit_point[0] - (space_spacing - letter_spacing)
    else :
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
        text_g_code += gcode_lib.move_fast(
            0, 0, -pass_depth, displacement_speed
        )
        text_g_code += character_g_code
        text_g_code += gcode_lib.move_fast(
            0, 0,  pass_depth, displacement_speed
        )
    old_exit_point = exit_point
g_code_file.write(text_g_code)

# ------------------------------------------------------------------------------
                                                                   # end of file
g_code_file.write("\n")
g_code_file.close()
