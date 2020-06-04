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
    """
    Returns true if line intersects the arc defined by center,
    radius, angles =[start, end] and orientation: +1 or -1
    Touching should not be considered intersecting
    If a line kisses the circle, it isn't instersecting it
    Touching endpoints is also okay, but only if it's both line and arc endpoint
    """

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
    if abs(lineY) >= radius:
        return False

    # The line intersects the circle at x values positive and negative xIntersection.
    xIntersection = np.sqrt(radius**2-abs(lineY)**2)

    candidates = []
    # Decide where the segment intersects the circle
    # Don't include line endpoints
    if (min(line[0][0], line[1][0]) < xIntersection and
            max(line[0][0], line[1][0]) > xIntersection):
        candidates.append(xIntersection)
    if (min(line[0][0], line[1][0]) < -xIntersection and
            max(line[0][0], line[1][0]) > -xIntersection):
        candidates.append(-xIntersection)

    # Check if any of the candidate xs is in the arc
    # Include endpoints
    for x in candidates:
        if isPointInSector([x, lineY], angleBegin, angleEnd,
                           orientation, includeBoundry=True):
            return True

    return False


def arcsIntersect(center1, radius1, angles1, orientation1,
                  center2, radius2, angles2, orientation2):
    """"
    Returns True if arcs intersect, otherwise false
    does not include endpoints nor not kissing
    """

    # Copy the arrays so that we don't change the originals
    center1 = center1.copy()
    center2 = center2.copy()
    angles1 = angles1.copy()
    angles2 = angles2.copy()

    # First, shift so that the first arc is centered on 0,0
    center2 -= center1

    # Rotate so that second arc is centered on (x,0)
    theta = np.arctan2(center2[1], center2[0])
    center2 = np.matmul(rotMat(-theta), center2)
    angles1 = (angles1 - theta) % (2 * np.pi)
    angles2 = (angles2 - theta) % (2 * np.pi)

    # If the circles are too far away from each other to intersect
    if center2[0] >= radius1 + radius2:
        return False
    # If one circle is completely inside another, they don't itersect
    # Circle2 is in circle1
    if radius1 >= center2[0] + radius2:
        return False
    # Circle1 is in circle2
    if radius2 >= center2[0] + radius1:
        return False

    # If the two centers overlap,
    # just check if the endpoints of one isn't in the other
    if all(center2 == np.array([0,0])):
        if radius1 != radius2:
            return False
        else:
            endPoint21 = np.matmul(rotMat(angles2[0]), [radius2, 0])
            endPoint22 = np.matmul(rotMat(angles2[1]), [radius2, 0])
            if isPointInSector(endPoint21, *angles1, orientation1):
                return True
            elif isPointInSector(endPoint22, *angles1, orientation1):
                return True
            endPoint11 = np.matmul(rotMat(angles1[0]), [radius1, 0])
            endPoint12 = np.matmul(rotMat(angles1[1]), [radius1, 0])
            if isPointInSector(endPoint11, *angles2, orientation2):
                return True
            elif isPointInSector(endPoint12, *angles2, orientation2):
                return True
            else:
                return False


    # Circles intesect at (x,y) and (x,-y)
    x = (center2[0]**2 + radius1**2 - radius2**2)/(2*center2[0])
    y = np.sqrt(radius1**2 - x**2)
    if np.isnan(y):
        breakpoint()

    # Check if the first interseciton is in both arcs
    if isPointInSector([x, y], angles1[0], angles1[1], orientation1,
                       includeBoundry=False):
        if isPointInSector([x - center2[0], y], angles2[0], angles2[1],
                           orientation2, includeBoundry=False):
            return True

    # Check if the second interseciton is in both arcs
    if isPointInSector([x, -y], angles1[0], angles1[1], orientation1,
                       includeBoundry=False):
        if isPointInSector([x - center2[0], -y], angles2[0], angles2[1],
                           orientation2, includeBoundry=False):
            return True

    return False


def isPointInSector(point, angleBegin, angleEnd, orientation,
                    includeBoundry=False):
    """
    Returns true if point is in the (infinite radius) sector
    defined by angleBegin, angleEnd and orientation
    does not include boundry by default, point on boundry not considered "in"
    """

    angleBegin %= (2 * np.pi)
    angleEnd %= (2 * np.pi)
    theta = np.arctan2(point[1], point[0]) % (2 * np.pi)

    # If orientation is negative, switch beginning and end, making it positive
    if orientation == -1:
        angleBegin, angleEnd = angleEnd, angleBegin

    if angleBegin < angleEnd:
        # 0 isn't included
        if includeBoundry:
            return angleBegin <= theta and theta <= angleEnd
        else:
            return angleBegin < theta and theta < angleEnd

    elif angleBegin == angleEnd:
        raise ValueError('zero length arc given')

    else:
        # 0 is included
        if includeBoundry:
            return theta <= angleEnd or angleBegin <= theta
        else:
            return theta < angleEnd or angleBegin < theta


def linesIntersect(line1, line2):
    """
    line arguments are on the form [[p1x, p1y], [p2x, p2y]]
    The line segments intersect if
    the scalar product of (the vector from p11 to p21) and (a vector normal to line1) and
    the scalar product of (the vector from p11 to p22) and (the vector normal to line1)
    have different signs
    AND vice versa, that is:
    the scalar product of (the vector from p21 to p11) and (a vector normal to line2)
    the scalar product of (the vector from p21 to p12) and (the vector normal to line2)
    have different signs
    p11 is the first point on line1 and so on.
    All arguments should be numpy arrays.

    Does NOT include endpoints
    """

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

    return (np.dot(vector1121, normalLine1) * np.dot(vector1122, normalLine1) < 0 and np.dot(vector2111, normalLine2) * np.dot(vector2112, normalLine2) < 0)
