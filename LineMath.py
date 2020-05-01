import numpy as np


def boxesIntersect(line1, line2):
    # If the smallest box around line 1 intersects the smallest box
    # around line 2, return true, else return false.
    return line1[0][0] <= line2[1][0] and line1[1][0] >= line2[0][0] and line1[0][1] <= line2[1][1] and line1[1][1] >= line2[0][1]


def segmentIntersectsArc(line, center, radius, angles):
    # Returns true if line intersects the arc defined py center
    # radius and angles, check https://math.stackexchange.com/questions/2744422/line-segment-and-arc-intersection
    pass


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
