import math

# ==============================================================================
                                                                # default values
default_drill_displacement_speed = 300
default_machining_parameters = {
    'displacement_height'      : 10,
    'drill_depth'              : 10,
    'pass_depth'               : 1,
    'drill_diameter'           : 4,
    'fast_displacement_speed'  : 1000,
    'drill_displacement_speed' : default_drill_displacement_speed,
    'drill_bore_speed'         : 500
}

# ==============================================================================
                                                                 # basic g-codes
# ..............................................................................
                                       # g-code for setting units to millimeters
def set_units_to_millimeters():
    return("G21 (set units to millimeters)\n")

# ..............................................................................
          # g-code for setting current position to the origin for absolute moves
def set_current_position_as_origin(set_x=True, set_y=True, set_z=False):
    position_ids = ''
    g_code = 'G92'
    if set_x:
        g_code += ' X0'
        position_ids += 'X'
    if set_y:
        g_code += ' Y0'
        if position_ids :
            position_ids += ',Y'
        else :
            position_ids += 'Y'
    if set_z:
        g_code += ' Z0'
        if position_ids :
            position_ids += ',Z'
        else :
            position_ids += 'Z'

    return(g_code + " (set %s position to zero)\n" % position_ids)

# ..............................................................................
                                                     # g-code for tool selection
def select_tool(drill_diameter):
    return(
        "T%.3g (drill diameter for the following operations)\n"
        % drill_diameter
    )

# ..............................................................................
                                               # g-code for absolute coordinates
def set_absolute_coordinates(absolute=True):
    if absolute :
        return("G90 (set to absolute positioning)\n")
    else :
        return("G91 (set to relative positioning)\n")

# ..............................................................................
                                               # g-code for relative coordinates
def set_relative_coordinates(relative=True):
    return(set_absolute_coordinates(not relative))

# ..............................................................................
                                                     # g-code for rapid movement
def move_fast(dx=0, dy=0, dz=0, speed=0, absolute=False):
    g_code = 'G0'
    if dx != 0 or absolute :
        g_code += " X%.3f" % dx
    if dy != 0 or absolute :
        g_code += " Y%.3f" % dy
    if dz != 0 :
        g_code += " Z%.3f" % dz
    if speed != 0 :
        g_code += " f%g" % speed

    if (g_code == 'G0') or g_code.startswith('G0 f') :
        return('')
    else :
        return(g_code + "\n")

# ..............................................................................
                                                    # g-code for linear movement
def move_steady(dx=0, dy=0, dz=0, speed=0):
    g_code = 'G1'
    if dx != 0 :
        g_code += " X%.3f" % dx
    if dy != 0 :
        g_code += " Y%.3f" % dy
    if dz != 0 :
        g_code += " Z%.3f" % dz
    if speed != 0 :
        g_code += " f%g" % speed

    if (g_code == 'G1') or g_code.startswith('G1 f') :
        return('')
    else :
        return(g_code + "\n")

# ..............................................................................
                                         # g-codes for moving back to the origin
def move_back_to_origin(move_x=True, move_y=True, move_z=False):
    g_code = "; move back to origin\n"
                                                # switch to absolute coordinates
    g_code += set_absolute_coordinates()
                                                             # move fast to zero
    g_code += 'G0'
    if move_x:
        g_code += ' X0'
    if move_y:
        g_code += ' Y0'
    if move_z:
        g_code += ' Z0'
    g_code += "\n"
                                           # switch back to relative coordinates
    g_code += set_relative_coordinates()

    return(g_code)

# ==============================================================================
                                                # basic horizontal g-code shapes
# ..............................................................................
                                                                          # line
def line_gcode(delta_x, delta_y, speed=default_drill_displacement_speed):
                                                                    # drill line
    g_code = move_steady(delta_x,delta_y, 0, speed)

    return(g_code)

# ..............................................................................
                                                                     # rectangle
def rectangle_gcode(base, height, speed=default_drill_displacement_speed):
    g_code = ''
                                                                   # drill sides
    g_code += move_steady( base,  0     , 0, speed)
    g_code += move_steady( 0   ,  height, 0, speed)
    g_code += move_steady(-base,  0     , 0, speed)
    g_code += move_steady( 0   , -height, 0, speed)

    return(g_code)

# ..............................................................................
                                                                        # circle
def circle_gcode(
    diameter, facet_nb=64, start_angle=0,
    speed=default_drill_displacement_speed
):
    g_code = ''
                                                                  # drill facets
    old_x = diameter/2 * math.cos(start_angle)
    old_y = diameter/2 * math.sin(start_angle)
    for index in range(1, facet_nb+1) :
        new_x = diameter/2 * math.cos(start_angle + index*2*math.pi/facet_nb)
        new_y = diameter/2 * math.sin(start_angle + index*2*math.pi/facet_nb)
        g_code += move_steady(new_x-old_x, new_y-old_y, 0, speed)
        old_x = new_x
        old_y = new_y

    return(g_code)

# ..............................................................................
                                                                        # circle
def circle_arc_gcode(
    radius, facet_nb=64, start_angle=0, end_angle=90,
    speed=default_drill_displacement_speed
):
    g_code = ''
    step_angle = (end_angle - start_angle)/facet_nb
                                                                  # drill facets
    old_x = radius * math.cos(start_angle)
    old_y = radius * math.sin(start_angle)
    for index in range(1, facet_nb+1) :
        new_x = radius * math.cos(start_angle + index*step_angle)
        new_y = radius * math.sin(start_angle + index*step_angle)
        g_code += move_steady(new_x-old_x, new_y-old_y, 0, speed)
        old_x = new_x
        old_y = new_y

    return(g_code)

# ..............................................................................
                                                                       # polygon
def polygon_gcode(
    polygon, close_shape=True,
    speed=default_drill_displacement_speed
):
    g_code = ''
                                                                   # drill lines
    old_x = 0
    old_y = 0
    for index in range(len(polygon)) :
        new_x = polygon[index][0]
        new_y = polygon[index][1]
        g_code += move_steady(new_x-old_x, new_y-old_y, 0, speed)
        old_x = new_x
        old_y = new_y
                                                                 # close polygon
    if close_shape:
        g_code += move_steady(-old_x, -old_y, 0, speed)

    return(g_code)

# ==============================================================================
                                                       # polygons and transforms
# ..............................................................................
                                                                     # rectangle
def build_retangle(x_offset, y_offset, x_length, y_length):
    coordinates = [
      [x_offset           , y_offset],
      [x_offset + x_length, y_offset           ],
      [x_offset + x_length, y_offset + y_length],
      [x_offset           , y_offset + y_length],
    ]

    return coordinates

# ..............................................................................
                              # regular convex polygon (fitting inside a circle)
def build_regular_polygon(diameter, facet_nb=64):
    coordinates = []

    for index in range(facet_nb) :
        x = diameter/2 * math.cos(2*index*math.pi/facet_nb)
        y = diameter/2 * math.sin(2*index*math.pi/facet_nb)
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                                         # polygon from svg file
def import_polygon(file_specification, polygon_id, close_path=False):
                                          # initial coordinate for relative mode
    coordinates = [[0, 0]]
                                                                     # read file
    svg_file = open(file_specification, 'r')
    svg_data = svg_file.read()
    svg_file.close()
                                                          # remove all line ends
    svg_data = svg_data.replace("\n", '')
                                                        # remove multiple spaces
    svg_data = ' '.join(svg_data.split())
                                                     # separate paths into lines
    replacements = {'<path ': "\n<path ", '/>': "/>\n"}
    for (source, replacement) in replacements.items() :
        svg_data = svg_data.replace(source, replacement)
                                                            # find selected path
    polygon_path = ''
    for path in svg_data.split("\n") :
        if path.startswith('<path ') :
            if (" id=\"%s\" " % polygon_id) in path :
                polygon_path = path
                                                         # keep only coordinates
    if polygon_path :
        polygon_path = polygon_path[polygon_path.find(' d="')+4 :]
        polygon_path = polygon_path[: polygon_path.find('"')]
                                                      # loop through description
        mode = ''
        command = ''
        for data in polygon_path.split(' ') :
            coordinate = ''
            if len(data) == 1 :
                command = ''
                if data == 'm' :
                    command = 'move to'
                    mode = 'relative'
                if data == 'M' :
                    command = 'move to'
                    mode = 'absolute'
                elif data == 'l' :
                    command = 'line to'
                    mode = 'relative'
                elif data == 'L' :
                    command = 'line to'
                    mode = 'absolute'
                elif data == 'h' :
                    command = 'horizontal line to'
                    mode = 'relative'
                elif data == 'H' :
                    command = 'horizontal line to'
                    mode = 'absolute'
                elif data == 'v' :
                    command = 'vertical line to'
                    mode = 'relative'
                elif data == 'V' :
                    command = 'vertical line to'
                    mode = 'absolute'
                elif (data == 'Z') or (data == 'z') :
                    command = 'close path'
            else :
                previous_x_coordinate = coordinates[-1][0]
                previous_y_coordinate = coordinates[-1][1]
                if (command == 'move to') or (command == 'line to') :
                    coordinate = data.split(',')
                    x_coordinate = float(coordinate[0])
                    y_coordinate = float(coordinate[1])
                    if mode == 'relative' :
                        x_coordinate = previous_x_coordinate + x_coordinate
                        y_coordinate = previous_y_coordinate + y_coordinate
                    coordinate = [x_coordinate, y_coordinate]
                elif command == 'horizontal line to' :
                    x_coordinate = float(data)
                    y_coordinate = previous_y_coordinate
                    if mode == 'relative' :
                        x_coordinate = previous_x_coordinate + x_coordinate
                    coordinate = [x_coordinate, y_coordinate]
                elif command == 'vertical line to' :
                    x_coordinate = previous_x_coordinate
                    y_coordinate = float(data)
                    if mode == 'relative' :
                        y_coordinate = previous_y_coordinate + y_coordinate
                    coordinate = [x_coordinate, y_coordinate]
            if coordinate :
                coordinates.append([x_coordinate, y_coordinate])
                                                                 # close polygon
        if (command == 'close path') and close_path :
            coordinates.append(coordinates[1])
                                               # remove first (dummy) coordinate
    coordinates = coordinates[1:]

    return(coordinates)

# ..............................................................................
                                          # min and max coordinates of a polygon
def min_max(polygon):
    x_min = polygon[0][0]
    y_min = polygon[0][1]
    x_max = x_min
    y_max = y_min

    for coordinate in polygon :
        [x, y] = coordinate
        x_min = min(x_min, x)
        y_min = min(y_min, y)
        x_max = max(x_max, x)
        y_max = max(y_max, y)

    return(x_min, y_min, x_max, y_max)

# ..............................................................................
                     # extract first coordinate of a polygon and offset the rest
def extract_offset(polygon, close_shape=True):
                                                  # offsets are first coordinate
    [x_offset, y_offset] = polygon[0]
    extracted_polygon = []
                                                              # take offset away
    for index in range(len(polygon)) :
        extracted_polygon.append(
            [polygon[index][0] - x_offset, polygon[index][1] - y_offset]
        )
                                                # remove first (zero) coordinate
    extracted_polygon = extracted_polygon[1:]
                                                                   # close shape
    if close_shape :
        extracted_polygon.append([0, 0])

    return(x_offset, y_offset, extracted_polygon)

# ..............................................................................
                                     # flip polygon vertically around the x-axis
def flip_vertical(polygon):
    coordinates = []

    for coordinate in polygon :
        x = coordinate[0]
        y = -coordinate[1]
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                   # flip polygon horizontally around the y-axis
def flip_horizontal(polygon):
    coordinates = []

    for coordinate in polygon :
        x = -coordinate[0]
        y = coordinate[1]
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                           # offset polygon by a constant vector
def offset_polygon(polygon, delta_x, delta_y):
    coordinates = []

    for coordinate in polygon :
        x = coordinate[0] + delta_x
        y = coordinate[1] + delta_y
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                                  # scale polygon by x-y factors
def scale_polygon(polygon, scale_x, scale_y=0):
    coordinates = []
    scale_y_effective = scale_y
    if scale_y == 0 :
        scale_y_effective = scale_x

    for coordinate in polygon :
        x = scale_x           * coordinate[0]
        y = scale_y_effective * coordinate[1]
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                       # rotate polygon around coordinate [0, 0]
def rotate_polygon(polygon, angle):
    coordinates = []

    for coordinate in polygon :
        amplitude = math.sqrt(coordinate[0]**2 + coordinate[1]**2)
        start_angle = math.atan2(coordinate[1], coordinate[0])
        x = amplitude * math.cos(angle + start_angle)
        y = amplitude * math.sin(angle + start_angle)
        coordinates.append([x, y])

    return coordinates

# ..............................................................................
                                           # expand polygon by a specified width
     # https://stackoverflow.com/questions/3749678/expand-fill-of-convex-polygon
def expand_polygon(polygon, distance):
    coordinates = []

    for index in range(len(polygon)) :
                                    # find previous, actual and next coordinates
        if index > 0 :
            x1 = polygon[index-1][0]
            y1 = polygon[index-1][1]
        else :
            x1 = polygon[-1][0]
            y1 = polygon[-1][1]
        x = polygon[index][0]
        y = polygon[index][1]
        if index < len(polygon)-1 :
            x2 = polygon[index+1][0]
            y2 = polygon[index+1][1]
        else :
            x2 = polygon[0][0]
            y2 = polygon[0][1]
                                                   # calculate parallel vector 1
        amplitude1 = math.sqrt((x-x1)**2 + (y-y1)**2)
        dx1 =  (y-y1)/amplitude1 * distance
        dy1 = -(x-x1)/amplitude1 * distance
        x1_p = x1 + dx1
        y1_p = y1 + dy1
        x_p1 = x + dx1
        y_p1 = y + dy1
                                                   # calculate parallel vector 2
        amplitude2 = math.sqrt((x2-x)**2 + (y2-y)**2)
        dx2 =  (y2-y)/amplitude2 * distance
        dy2 = -(x2-x)/amplitude2 * distance
        x_p2 = x + dx2
        y_p2 = y + dy2
        x2_p = x2 + dx2
        y2_p = y2 + dy2
                                                  # calculate lines intersection
        if x_p1 == x1_p :    # first line vertical
            b1 = x_p1
            a2 = (y_p2 - y2_p) / (x_p2 - x2_p)
            b2 = y_p2 - a2*x_p2
            x_intersection = b1
            y_intersection = a2*b1 + b2
        elif x_p2 == x2_p :    # second line vertical
            a1 = (y_p1 - y1_p) / (x_p1 - x1_p)
            b1 = y_p1 - a1*x_p1
            b2 = x_p2
            x_intersection = b2
            y_intersection = a1*b2 + b1
        else :
            a1 = (y_p1 - y1_p) / (x_p1 - x1_p)
            b1 = y_p1 - a1*x_p1
            a2 = (y_p2 - y2_p) / (x_p2 - x2_p)
            b2 = y_p2 - a2*x_p2
            x_intersection = (b2 - b1) / (a1 - a2)
            y_intersection = (a2*b1 - a1*b2) / (a2 - a1)
                                                                # append to list
        coordinates.append([x_intersection, y_intersection])

    return coordinates

# ..............................................................................
                                 # find hole set for compensating drill diameter
def find_hole_set(polygon, start_angle=0):
    holes = []

    for index in range(len(polygon)) :
        if index > 0 :
            x_p = polygon[index-1][0]
            y_p = polygon[index-1][1]
        else :
            x_p = polygon[-1][0]
            y_p = polygon[-1][1]
        x = polygon[index][0]
        y = polygon[index][1]
        if index < len(polygon)-1 :
            x_n = polygon[index+1][0]
            y_n = polygon[index+1][1]
        else :
            x_n = polygon[0][0]
            y_n = polygon[0][1]
        angle_p = math.atan2(y-y_p, x-x_p)
        angle_n = math.atan2(y_n-y, x_n-x)
        turn_angle = angle_n - angle_p
        if turn_angle > math.pi :
            turn_angle = turn_angle - 2*math.pi
        if turn_angle < -math.pi :
            turn_angle = turn_angle + 2*math.pi
        #print(turn_angle*180/math.pi)
        if turn_angle < start_angle :
            #print("%g => [%g, %g]" % (turn_angle*180/math.pi, x, y))
            holes.append([x, y])

    return holes

# ..............................................................................
                                    # find if a coordinate is between two others
def are_in_row(x1, x, x2):
    x_is_between = False
    if ( (x1 <= x) and (x <= x2) ) or ( (x2 <= x) and (x <= x1) ) :
        x_is_between = True

    return x_is_between

# ..............................................................................
                                 # find intersection between segment and polygon
def segment_polygon_intersection(segment, polygon):
    coordinates = []
    intersections = []
                                                           # segment coordinates
    [x1, y1] = segment[0]
    [x2, y2] = segment[1]
                                              # special case of vertical segment
    if x1 == x2 :
#        print("x1 = x2 = %g" % x1)
        for index in range(len(polygon)-1) :
            [x_a, y_a] = polygon[index]
            [x_b, y_b] = polygon[index+1]
#            print([x_a, y_a])
            if are_in_row(x_a, x1, x_b) :
                a = (y_b-y_a) / (x_b-x_a)
                b = y_a - a*x_a
                x_i = x1
                y_i = a*x_i + b
                if are_in_row(y1, y_i, y2) :
                    coordinates.append([x_i, y_i])
                    intersections.append(index)
                                            # special case of horizontal segment
# not tested yet
    elif y1 == y2 :
#        print("y1 = y2 = %g" % y1)
        for index in range(len(polygon)-1) :
            [x_a, y_a] = polygon[index]
            [x_b, y_b] = polygon[index+1]
#            print([x_a, y_a])
            if are_in_row(y_a, y1, y_b) :
                           # very special case of a horizontal-vertical crossing
                if x_a == x_b :
                    x_i = x_a
                    y_i = y1
                                 # horizontal segment crossing non-infinite sope
                else :
                    a = (y_b-y_a) / (x_b-x_a)
                    b = y_a - a*x_a
                    y_i = y1
                    x_i = (y_i - b) / a
                if are_in_row(y1, y_i, y2) :
                    coordinates.append([x_i, y_i])
                    intersections.append(index)
                                   # segment with non-zero and non-infinite sope
    else :
        for index in range(len(polygon)-1) :
            [x_a, y_a] = polygon[index]
            [x_b, y_b] = polygon[index+1]
                                      # special case of vertical polygon segment
# not tested yet
            if (x_a == x_b) and (x1 == x_a) :
                coordinates.append([x1, y1])
                intersections.append(index)
                                                                  # generic case
            else :
                a_s = (y2-y1) / (x2-x1)
                b_s = y1 - a_s*x1
                y_a1 = a_s*x_a + b_s
                y_b1 = a_s*x_b + b_s
                if                                          \
                    ( (y_a1 < y_a) and (y_b1 > y_b) ) or    \
                    ( (y_a1 > y_a) and (y_b1 < y_b) )       \
                :
                    a = (y_b-y_a) / (x_b-x_a)
                    b = y_a - a*x_a
                    x_i = (b_s-b) / (a-a_s)
                    y_i = a*x_i + b
                    if are_in_row(y_a, y_i, y_b) :
                        coordinates.append([x_i, y_i])
                        intersections.append(index)

    return(coordinates, intersections)

# ==============================================================================
                                                               # drill sequences
# ..............................................................................
                                                # g-code for initial positioning
def go_to_start(
    start_x=0, start_y=0,
    machining_parameters=default_machining_parameters,
    machine=''
):
    displacement_height      = machining_parameters['displacement_height']
    fast_displacement_speed  = machining_parameters['fast_displacement_speed']
    drill_displacement_speed = machining_parameters['drill_displacement_speed']

    g_code = ";\n; initialization\n;\n"
    if machine == 'X_Carve' :
        g_code += "$102=189 (X-Carve vertical axis displacement setup)\n"
    elif machine == 'Next3D' :
        g_code += "$102=133 (Next3D vertical axis displacement setup)\n"
    g_code += set_units_to_millimeters()
    g_code += set_current_position_as_origin(False, False, True)
    g_code += set_relative_coordinates()
    g_code += "; move up to displacement height, set steady pace\n"
    g_code += move_steady(0, 0, displacement_height, drill_displacement_speed)
    g_code += "; move to start position, set fast pace\n"
    g_code += move_fast(start_y, start_y, 0, fast_displacement_speed)
    g_code += set_current_position_as_origin(True, True, False)

    return(g_code)

# ..............................................................................
                                                          # build drill sequence
def build_drawing_element(
    drill_g_code,
    start_x=0, start_y=0,
    machining_parameters=default_machining_parameters,
    comment=''
):
    displacement_height     = machining_parameters['displacement_height']
    drill_depth             = machining_parameters['drill_depth']
    pass_depth              = machining_parameters['pass_depth']
    drill_diameter          = machining_parameters['drill_diameter']
    fast_displacement_speed = machining_parameters['fast_displacement_speed']
    drill_bore_speed        = machining_parameters['drill_bore_speed']
    g_code = ''
                                                                   # add comment
    if comment != '' :
        g_code += '; ' + comment + "\n"
                                                             # select tool width
    if drill_diameter > 0 :
        g_code += select_tool(drill_diameter)
                                                                # move to origin
    if (start_x != 0) or (start_y != 0) :
        g_code += move_fast(start_x, start_y, 0, fast_displacement_speed)
                                                                   # single pass 
    if pass_depth == 0 :
        g_code += move_steady(
            0, 0, -displacement_height-drill_depth, drill_bore_speed
        )
        g_code += drill_g_code
                                                         # multiple passes drill
    else :
        g_code += move_steady(0, 0, -displacement_height, drill_bore_speed)
        pass_nb = math.ceil(drill_depth/pass_depth)
        for index in range(pass_nb-1) :
            g_code += move_steady(0, 0, -pass_depth, drill_bore_speed)
            g_code += drill_g_code
        remaining_depth = drill_depth - (pass_nb-1)*pass_depth
        g_code += move_steady(0, 0, -remaining_depth, drill_bore_speed)
        g_code += drill_g_code
                                                # back up to displacement height
    g_code += move_fast(
        0, 0, drill_depth+displacement_height, fast_displacement_speed
    )

    return g_code

# ..............................................................................
                                                   # drill set of vertical holes
def build_hole_set(
    hole_set,
    machining_parameters=default_machining_parameters,
    comment=''
):
    displacement_height     = machining_parameters['displacement_height']
    drill_depth             = machining_parameters['drill_depth']
    drill_diameter          = machining_parameters['drill_diameter']
    fast_displacement_speed = machining_parameters['fast_displacement_speed']
    drill_bore_speed        = machining_parameters['drill_bore_speed']

    g_code = ''
                                                                   # add comment
    if comment != '' :
        g_code += '; ' + comment + "\n"
                                                             # select tool width
    if drill_diameter > 0 :
        g_code += select_tool(drill_diameter)
                                                                   # loop on set
    [old_x, old_y] = [0, 0]
    for hole_coordinate in hole_set:
        [x, y] = hole_coordinate
        g_code += move_fast(x-old_x, y-old_y, 0, fast_displacement_speed)
        g_code += move_steady(
            0, 0, -displacement_height-drill_depth, drill_bore_speed
        )
        g_code += move_fast(
            0, 0, drill_depth+displacement_height, fast_displacement_speed
        )
        old_x = x
        old_y = y
  
    return g_code

# ..............................................................................
                                      # drill set of lines with drill tool width
def build_slit_set(
    start_x=0, start_y=0,
    dx=0, dy=0, x_spacing=0, y_spacing=0, slit_nb=1,
    machining_parameters=default_machining_parameters,
    comment=''
):
    displacement_height      = machining_parameters['displacement_height']
    drill_depth              = machining_parameters['drill_depth']
    pass_depth               = machining_parameters['pass_depth']
    drill_diameter           = machining_parameters['drill_diameter']
    fast_displacement_speed  = machining_parameters['fast_displacement_speed']
    drill_displacement_speed = machining_parameters['drill_displacement_speed']
    drill_bore_speed         = machining_parameters['drill_bore_speed']

    g_code = ''
                                                                   # add comment
    if comment != '' :
        g_code += '; ' + comment + "\n"
                                                             # select tool width
    if drill_diameter > 0 :
        g_code += select_tool(drill_diameter)
                                                                # move to origin
    if (start_x != 0) or (start_y != 0) :
        g_code += move_fast(start_x, start_y, 0, fast_displacement_speed)
                                                                         # slits
    for slit_index in range(slit_nb) :
        if slit_nb > 1 :
            g_code += "; slit %d\n" % (slit_index + 1)
        g_code += move_fast(0, 0, -displacement_height, fast_displacement_speed)
        double_pass_nb = math.ceil(drill_depth/(2*pass_depth))
        for pass_index in range(double_pass_nb) :
            g_code += move_steady(0, 0, -pass_depth, drill_bore_speed)
            g_code += move_steady(dx, dy, 0, drill_displacement_speed)
            g_code += move_steady(0, 0, -pass_depth, drill_bore_speed)
            g_code += move_steady(-dx, -dy, 0, drill_displacement_speed)
        g_code += move_steady(
            0, 0, 2*double_pass_nb*pass_depth, fast_displacement_speed
        )
        g_code += move_fast(0, 0, displacement_height, fast_displacement_speed)
        if slit_index+1 < slit_nb :
            g_code += move_fast(
                x_spacing, y_spacing, 0, fast_displacement_speed
            )

    return(g_code)
