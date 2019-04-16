def line_intersect(x1, y1, x2, y2, x3, y3, x4, y4):
    # hat tip: http://paulbourke.net/geometry/pointlineplane/
    if ((x1 == x2 and y1 == y2) or (x3 == x4 and y3 == y4)):
        return False

    denominator = ((y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1))

    if denominator == 0:
        return False

    ua = ((x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)) / denominator
    ub = ((x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)) / denominator

    # is the intersection along the segments
    if ua <= 0 or ua > 1 or ub <= 0 or ub > 1:
        return False

    # Return a object with the x and y coordinates of the intersection
    x = x1 + ua * (x2 - x1)
    y = y1 + ua * (y2 - y1)

    return x, y


def point_in_uv(x, y):
    return x <= 1 and x >= 0 and y <= 1 and y >= 0


def line_intersects_uv(x0, x1, y0, y1):
    lines = (
        (0, 0, 1, 0),
        (0, 0, 0, 1),
        (0, 1, 1, 1),
        (1, 0, 1, 1),
    )
    intersections = []
    for line in lines:
        intersection = line_intersect(x0, x1, y0, y1, *line)
        if intersection and point_in_uv(*intersection):
            intersections.append(intersection)


    return intersections
