import numpy as np


def rotMat(theta):
    # Returns a rotation matrix that rotates vectors around (0,0)
    s = np.sin(theta)
    c = np.cos(theta)
    return np.array([[c, -s],
                     [s, c]])


def boxesIntersect(line1, line2):
    # If the smallest box around line 1 intersects the smallest box
    # around line 2, return true, else return false.
    return line1[0][0] <= line2[1][0] and line1[1][0] >= line2[0][0] and line1[0][1] <= line2[1][1] and line1[1][1] >= line2[0][1]


def segmentIntersectsArc(line, center, radius, angles, orientation):
    # Returns true if line intersects the arc defined by center,
    # radius, angles =[start, end] and orientation: +1 or -1
    # Touching at endpoint is not intersecting, e.g. a line ending at a
    # point on the circle arc beginning will not be considered intersecting

    # If orientation is -1, switch angleIn and angleOut
    if orientation == -1:
        angles = angles[::-1]

    # Translate so that arc center is at 0, 0
    line = line - center

    # Rotate so that line is horizontal
    theta = np.arctan2(line[1][1] - line[0][1], line[1]
                       [0] - line[0][0]) % (2 * np.pi)
    line = np.array([np.matmul(rotMat(-theta), point) for point in line])
    lineY = line[0][1]
    angleBegin = (angles[0] - theta) % (2 * np.pi)
    angleEnd = (angles[1] - theta) % (2 * np.pi)

    # If the line does not intersect the circle, it definitely doesn't
    # intersect the arc
    if abs(lineY) > radius:
        return False

    # The line intersects the circle at x values positive and negative xIntersection.
    xIntersection = np.sqrt(radius**2-abs(lineY)**2)

    candidates = []
    # Decide where the segment intersects the circle
    if (min(line[0][0], line[1][0]) < xIntersection and
            max(line[0][0], line[1][0]) > xIntersection):
        candidates.append(xIntersection)
    if (min(line[0][0], line[1][0]) < -xIntersection and
            max(line[0][0], line[1][0]) > -xIntersection):
        candidates.append(-xIntersection)

    if not candidates:
        return False

    for x in candidates:
        phi = np.arctan2(lineY, x) % (2 * np.pi)
        if angleBegin < angleEnd:
            # Arc does not go across 0
            if angleBegin < phi and phi < angleEnd:
                return True
        else:
            # Arc does go across 0 angle, making begin and end angles opposite
            # Theta is in arc if it is greater than begin or less than end
            if phi > angleBegin or phi < angleEnd:
                return True

    return False


def linesIntersect(line1, line2):
    # line arguments are on the form [[p1x, p1y], [p2x, p2y]]
    # The line segments intersect if
    # the scalar product of (the vector from p11 to p21) and (a vector normal to line1) and
    # the scalar product of (the vector from p11 to p22) and (the vector normal to line1)
    # have different signs
    # AND vice versa, that is:
    # the scalar product of (the vector from p21 to p11) and (a vector normal to line2)
    # the scalar product of (the vector from p21 to p12) and (the vector normal to line2)
    # have different signs
    # p11 is the first point on line1 and so on.
    # All arguments should be numpy arrays.

    # Does the function inlude endpoints? I think so

    vector1121 = line1[0] - line2[0]
    vector1122 = line1[0] - line2[1]
    vector2111 = -vector1121
    vector2112 = line2[0] - line1[1]
    vectorLine1 = line1[1] - line1[0]
    vectorLine2 = line2[1] - line2[0]
    normalLine1 = np.array([vectorLine1[1], -vectorLine1[0]])
    normalLine2 = np.array([vectorLine2[1], -vectorLine2[0]])

    if (vectorLine1[0] == 0 and vectorLine1[1] == 0) or (vectorLine2[0] == 0 and vectorLine2[1] == 0):
        #print("One of the vectors are zero, returning False")
        return False

    return (np.dot(vector1121, normalLine1) * np.dot(vector1122, normalLine1) <= 0 and np.dot(vector2111, normalLine2) * np.dot(vector2112, normalLine2) <= 0)
