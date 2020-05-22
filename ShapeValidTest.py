from Shape import Shape
from LineMath import linesIntersect
from LineMath import segmentIntersectsArc
import numpy as np


def rotMat(theta):
    # Returns a rotation matrix that rotates vectors around (0,0)
    s = np.sin(theta)
    c = np.cos(theta)
    return np.array([[c, -s],
                     [s, c]])


def isThrough(shape, pos, rot):
    # Returns True if the shape transposed by pos and rotated
    # (in the positive direction) by rot is through the corridor
    for node in shape.nodes:
        # if node is outside shape, continue
        if not node.o == shape.o:
            continue
        if (np.matmul(rotMat(rot), node.pos) + pos)[1] - node.r < -0.5:
            return False

    # No node (after trasposition and rotation) was below -0.5
    return True


def isInBounds(shape, pos, rot):
    # Returns True if no part of shape is outside of corridor
    # Facts used: There is no need to check if lines cross the outer border,
    # if they did, that necessarily means a node is outside the outer border
    for node in shape.nodes:
        # Calculate the position of the node
        nodePos = np.matmul(rotMat(rot), node.pos) + pos
        # If the node is inside the shape
        if node.o == shape.o:
            # If node is outside outer bounds
            if nodePos[1] + node.r > 0.5 or nodePos[0] - node.r < -0.5:
                return False
            # If the inner corner (0.5,-0.5) is inside node
            cornerPos = np.array([0.5, -0.5])
            if np.linalg.norm(nodePos-cornerPos) < node.r:
                return False
            # If the node is below the corner and outside inner line
            if nodePos[1] < -0.5 and nodePos[0] + node.r > 0.5:
                return False
            # If the node is past the corner and below inner line
            if nodePos[0] > 0.5 and nodePos[1] - node.r < -0.5:
                return False
        # If node is outside the shape
        # An outside node can never be causing trouble at the outer wall
        else:
            # If arc of node intersects lower inner line,
            # TODO No need to check upper inner line?
            innerLine = np.array([[0.5, -0.5], [0.5, -100]])
            if segmentIntersectsArc(innerLine, nodePos, node.r, shape.nodeAngles[node.ID] + rot, node.o):
                return False

    # No nodes are bad if you got here
    # Now test if any of the binding lines cross the inner line
    innerLine = np.array([[0.5, -100], [0.5, -0.5]])
    for line in shape.lines:
        # Shift line
        line = np.array(
            [np.matmul(rotMat(rot), point) + pos for point in line])
        # Check if line crosses the inner line
        if linesIntersect(line, innerLine):
            return False

    # All tests passed, the shape is in bounds
    return True


def nodesOutOfBounds(shape, pos, rot):
    # Return node ids of (inside) nodes out of bounds
    # Also which quadrant they are out of bounds in

    #   II  :   I
    # .......:________
    #       |   0
    #   III |   ._____
    #       |   |
    #       |   | IV

    rvList = []

    for node in shape.nodes:
        # If node is not an inside node, continue
        if node.o != shape.o:
            continue

        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        if nodePos[1] + node.r > 0.5:
            rvList.append([node.ID, 1])
        if nodePos[0] - node.r < -0.5:
            rvList.append([node.ID, 3])
        if nodePos[0] - node.r < -0.5 and nodePos[1] + node.r > 0.5:
            rvList.append([node.ID, 2])
        if nodePos[0] + node.r > 0.5 and nodePos[1] <= -0.5:
            rvList.append([node.ID, 4])
        elif nodePos[1] - node.r < -0.5 and nodePos[0] >= 0.5:
            rvList.append([node.ID, 4])
        elif np.linalg.norm(nodePos - np.array([0.5, -0.5])) < node.r:
            rvList.append([node.ID, 4])

    return rvList


def shapeIsValid(shape):
    # Returns true if shape can be moved through a corridor with
    # width 1 and a 90 degree turn to the right
    # The corridor is initially centered on 0

    # Check if shape is within constraints to begin with
    # For each node, check that the edge of the node is within x=-0.5 and x=0.5
    # Also note where the top of the shape is
    maximumY = 0
    for node in shape.nodes:
        if node.pos[0] + node.r > 0.5 or node.pos[0] - node.r < -0.5:
            return False

        if node.pos[1] > maximumY:
            maximumY = node.pos[1]

    # Place shape so that no part of it is beyond the beginning of the turn
    position = -0.5 - maximumY
    rotation = 0

    #while True:
