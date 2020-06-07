from Shape import Shape
from LineMath import linesIntersect
from LineMath import segmentIntersectsArc
import numpy as np


def rotMat(theta):
    """ Returns a rotation matrix that rotates vectors around (0,0) """
    s = np.sin(theta)
    c = np.cos(theta)
    return np.array([[c, -s],
                     [s, c]])


def isThrough(shape, pos, rot):
    """
    Returns True if the shape transposed by pos and rotated
    (in the positive direction) by rot is through the corridor
    """

    # Tolerance to remove funky business with machine precision errors
    tol = 1e-13

    # Make lines
    lowerLine = np.array([[-0.5, -0.5 - tol], [100, -0.5 - tol]])
    upperLine = np.array([[-0.5, 0.5 + tol], [100, 0.5 + tol]])
    leftyLine = np.array([[-0.5 - tol, -0.5], [-0.5 - tol,  0.5]])

    for node in shape.nodes:
        # Calculate the position of the node
        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        # Check if the relevant part of the node intersects the lines
        if segmentIntersectsArc(lowerLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False
        if segmentIntersectsArc(upperLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False
        if segmentIntersectsArc(leftyLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False

    # No nodes are bad if you got here
    # Now test if any of the binding lines cross the lines
    for line in shape.lines:
        # Shift line
        line = np.array(
            [np.matmul(rotMat(rot), point) + pos for point in line])
        # Check if line crosses the inner line
        if linesIntersect(line, lowerLine):
            return False
        if linesIntersect(line, upperLine):
            return False
        if linesIntersect(line, leftyLine):
            return False

    # All tests passed, the shape is in bounds
    return True


def isInBounds(shape, pos, rot):
    "Returns True if no part of shape is outside of corridor"

    # Tolerance to remove funky business with machine precision errors
    tol = 1e-13

    # Make lines
    innerLowerLine = np.array([[0.5 + tol, -0.5], [0.5 + tol, -100]])
    innerUpperLine = np.array([[0.5, -0.5 - tol], [100, -0.5 - tol]])
    outerLowerLine = np.array([[-0.5 - tol, 0.5], [-0.5 - tol, -100]])
    outerUpperLine = np.array([[-0.5, 0.5 + tol], [100,  0.5 + tol]])

    for node in shape.nodes:
        # Calculate the position of the node
        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        # Check if the relevant part of the node intersects the lines
        if segmentIntersectsArc(innerLowerLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False
        if segmentIntersectsArc(innerUpperLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False
        if segmentIntersectsArc(outerLowerLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False
        if segmentIntersectsArc(outerUpperLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            return False

    # No nodes are bad if you got here
    # Now test if any of the binding lines cross the lines
    for line in shape.lines:
        # Shift line
        line = np.array(
            [np.matmul(rotMat(rot), point) + pos for point in line])
        # Check if line crosses the inner line
        if linesIntersect(line, innerLowerLine):
            return False
        if linesIntersect(line, innerUpperLine):
            return False
        if linesIntersect(line, outerLowerLine):
            return False
        if linesIntersect(line, outerUpperLine):
            return False

    # All tests passed, the shape is in bounds
    return True


def nodesOutOfBounds(shape, pos, rot):
    """
    Return node ids of (inside) nodes out of bounds
    Also which quadrant they are out of bounds in

    #    II  :   I
    # .......:________
    #        |   0
    #    III |   ._____
    #        |   |
    #        |   | IV
    """

    rvList = []

    # Because of comparing floats, we need a tolerance for machine
    # precision magnitude of errors
    tol = 1e-13

    # Make lines
    innerLowerLine = np.array([[0.5 + tol, -0.5], [0.5 + tol, -100]])
    innerUpperLine = np.array([[0.5, -0.5 - tol], [100, -0.5 - tol]])
    outerLowerLine = np.array([[-0.5 - tol, 0.5], [-0.5 - tol, -100]])
    outerUpperLine = np.array([[-0.5, 0.5 + tol], [100,  0.5 + tol]])

    for node in shape.nodes:
        # Calculate the position of the node
        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        intersectFound = False
        # Check if the relevant part of the node intersects the lines
        if segmentIntersectsArc(innerLowerLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            rvList.append([node.ID, 4])
            intersectFound = True
        if segmentIntersectsArc(innerUpperLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            rvList.append([node.ID, 4])
            intersectFound = True
        if segmentIntersectsArc(outerLowerLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            rvList.append([node.ID, 3])
            intersectFound = True
        if segmentIntersectsArc(outerUpperLine, nodePos, node.r,
                                shape.nodeAngles[node.ID] + rot, node.o):
            rvList.append([node.ID, 1])
            intersectFound = True
        if not intersectFound:
            # Calculate an endpoint (if no intersect was found,
            # both endpoints are either out of bounds or in bounds)
            endpoint = nodePos + \
                np.array([np.cos(shape.nodeAngles[node.ID][0] + rot),
                          np.sin(shape.nodeAngles[node.ID][0] + rot)]) * node.r

            if endpoint[1] > 0.5 + tol:
                rvList.append([node.ID, 1])
            if endpoint[0] < -0.5 - tol:
                rvList.append([node.ID, 3])
            if endpoint[0] < -0.5 - tol and endpoint[1] > 0.5 + tol:
                rvList.append([node.ID, 2])
            if endpoint[0] > 0.5 + tol and endpoint[1] <= -0.5:
                rvList.append([node.ID, 4])

    return rvList


def posRotToShiftTwoNodes(nodePos1, nodePos2, delta1, delta2):
    """
    Takes two nodes' (original) positions and where to move them
    Returns deltaPos and deltaRot that will acomplish this
    """

    # Calculate rotation
    vector12 = nodePos2 - nodePos1
    origAngle = np.arctan2(vector12[1], vector12[0])
    newVector12 = nodePos2 + delta2 - (nodePos1 + delta1)
    newAngle = np.arctan2(newVector12[1], newVector12[0])
    deltaRot = newAngle - origAngle

    # Calculate translation
    vectorOldNew1 = np.matmul(rotMat(deltaRot),
                              nodePos2 + delta2 - (nodePos1 + delta1))
    deltaPos = vectorOldNew1

    return (deltaPos, deltaRot)


def posRotToRotateAroundNode(shape, currentRot, theta, nodeID):
    """
    Takes (original) position around which we wish to rotate
    And theta, the (signed) angle we wish to rotate with
    Returns the pos and rot that accomplishes this
    """

    deltaRot = theta
    origNodePos = np.matmul(rotMat(currentRot), shape.nodes[nodeID].pos)
    newNodePos = np.matmul(rotMat(theta), origNodePos)
    deltaPos = origNodePos - newNodePos
    return (deltaPos, deltaRot)


def posRotToShiftRightWithRot(shape, pos, rot):
    """
    Returns the deltapos and deltarot required to shift shape
    right by stepRight
    If it isn't possible, returns None.
    """

    stepRight = 0.01
    stepRot = -0.01

    # Move shape right
    newPos = pos + np.array([stepRight, 0])
    newRot = rot

    # Get the top node
    topNodeID = getTopNodeId(shape, newPos, rot)

    # While shape is not in bounds, rotate cw until it is
    # or something new goes out of bounds
    while not isInBounds(shape, newPos, newRot):
        deltaPos, deltaRot = posRotToRotateAroundNode(
            shape, newRot, stepRot, topNodeID)

        # Check all of the out of bounds (inside) nodes
        for nodeWithQuadrant in nodesOutOfBounds(shape, newPos + deltaPos,
                                                 newRot + deltaRot):
            # If anyone went out to quadrant I, rotate around that one
            # instead next pass
            if nodeWithQuadrant[1] == 1:
                topNodeID = nodeWithQuadrant[0]
                break

            # If anyone is out in quadrant III, the game is lost
            # because then we can't rotate so that the shape clears
            # the corner and the leftest wall
            if nodeWithQuadrant[1] == 3:
                return None
        else:     # If for loop not broken
            newPos += deltaPos
            newRot += deltaRot

    return (newPos - pos, newRot - rot)


def posRotToRotateCWWithShift(shape, pos, rot):
    """
    Returns the deltapos and deltarot required to rotate shape CW
    by stepRot
    If it isn't possible, returns None.
    """
    stepMove = 0.01
    stepRot = -0.01

    newPos = pos.copy()
    newRot = rot

    # Rotate shape cw by stepRot around top node
    topNodeID = getTopNodeId(shape, newPos, rot)
    deltaPos, deltaRot = posRotToRotateAroundNode(
        shape, newRot, stepRot, topNodeID)
    newPos += deltaPos
    newRot += deltaRot

    # if some other node is now top node,
    # shift down so that that node is in bounds
    newTopNodeID = getTopNodeId(shape, newPos, newRot)
    if newTopNodeID != topNodeID:
        maximumY = (np.matmul(rotMat(newRot), shape.nodes[newTopNodeID].pos) +
                    pos)[1] + shape.nodes[newTopNodeID].r
        newPos[1] = 0.5 - maximumY

    # While shape is out of bounds, move back until it isn't
    # or it has gone out of bounds in Q III
    while not isInBounds(shape, newPos, newRot):

        # Check all of the out of bounds (inside) nodes
        for nodeWithQuadrant in nodesOutOfBounds(shape,
                                                 newPos - [stepMove, 0],
                                                 newRot):

            # If anyone is out in quadrant III, the game is lost
            # because then we can't back up more
            if nodeWithQuadrant[1] == 3:
                return None
        else:     # If for loop not broken
            newPos -= [stepMove, 0]

    return (newPos - pos, newRot - rot)


def shapeIsValid(shape):
    """
    Returns true if shape can be moved through a corridor with
    width 1 and a 90 degree turn to the right
    The corridor is initially centered on 0
    """

    topNode = shape.nodes[getTopNodeId(shape)]
    maximumY = topNode.pos[1] + topNode.r
    rightNode = shape.nodes[getRightNodeId(shape)]
    minimumX = rightNode.pos[0] - rightNode.r

    # Place shape as far up and as far left as possible
    pos = [-0.5 - minimumX, 0.5 - maximumY]
    rot = 0

    # Check that it is in bounds to begin with
    for node in shape.nodes:
        if node.o != shape.o:
            continue
        elif node.pos[0] + pos[0] + node.r > 0.5 or \
                node.pos[0] + pos[0] - node.r < -0.5:
            return False

    while True:
        deltaPosRot = posRotToShiftRightWithRot(shape, pos, rot)

        # If it can't be done, return False
        if deltaPosRot is None:
            return False
        # If the rotation is too big,
        # go back until we can rotate a little instead
        elif deltaPosRot[1] > 0.02:
            deltaPosRot = posRotToRotateCWWithShift(shape, pos, rot)

            # If it can't be done, return False
            if deltaPosRot is None:
                return False

        pos += deltaPosRot[0]
        rot += deltaPosRot[1]

        if isThrough(shape, pos, rot):
            return True
        # If we've rotated more than one full revolution, return false
        elif abs(rot) > 2 * np.pi:
            return False


def getWalk(shape):
    """
    Returns a sequence of positions and rotations that will get
    the shape through a corrodor with
    width 1 and a 90 degree turn to the right
    The corridor is centered on 0
    """

    topNode = shape.nodes[getTopNodeId(shape)]
    maximumY = topNode.pos[1] + topNode.r
    rightNode = shape.nodes[getRightNodeId(shape)]
    minimumX = rightNode.pos[0] - rightNode.r

    # Place shape as far left as possible and below the starting line
    pos = [-0.5 - minimumX, -0.5 - maximumY]
    rot = 0

    # Initialize arrays to hold positions and rotations
    poss = [pos.copy()]
    rots = [rot]

    # Check that it is in bounds to begin with
    if not isInBounds(shape, pos, rot):
        return (poss, rots)

    # Move up
    for y in np.linspace(-0.5 - maximumY, 0.5 - maximumY, 10):
        poss.append([pos[0], y])
        rots.append(0)

    # Place shape as far up and as far left as possible
    pos = [-0.5 - minimumX, 0.5 - maximumY]

    while True:
        deltaPosRot = posRotToShiftRightWithRot(shape, pos, rot)

        # If it can't be done, return
        if deltaPosRot is None:
            return (poss, rots)

        # If the rotation is too big,
        # go back until we can rotate a little instead
        elif deltaPosRot[1] < -0.02:
            deltaPosRot = posRotToRotateCWWithShift(shape, pos, rot)

            # If it can't be done, return
            if deltaPosRot is None:
                return (poss, rots)

            # If the jump in position is large, split it up
            if deltaPosRot[0][0] < -0.05:
                for x in np.arange(pos[0], pos[0] + deltaPosRot[0][0], -0.05):
                    poss.append([x, pos[1]])
                    rots.append(rot)

        pos += deltaPosRot[0]
        rot += deltaPosRot[1]
        poss.append(pos.copy())
        rots.append(rot)

        if isThrough(shape, pos, rot):
            # Move right until through the last part
            rightNode = shape.nodes[getRightNodeId(shape, pos, rot)]
            minimumX = np.matmul(rotMat(rot), rightNode.pos)[0] + \
                pos[0] - rightNode.r

            for x in np.arange(pos[0], pos[0] + 0.5 - minimumX + 0.05, 0.05):
                poss.append([x, pos[1]])
                rots.append(rot)

            return (poss, rots)

        # If we've rotated more than one full revolution, return
        elif abs(rot) > 2 * np.pi:
            return (poss, rots)


def getTopNodeId(shape, pos=np.array([0, 0]), rot=0):
    """
    Returns the id of the (inside) node that reaches the
    highest y-value
    """

    maximumY = None
    topNodeID = None
    for node in shape.nodes:
        # If node isn't inside node
        if node.o != shape.o:
            continue

        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        if maximumY is None or nodePos[1] + node.r > maximumY:
            maximumY = nodePos[1] + node.r
            topNodeID = node.ID

    return topNodeID


def getRightNodeId(shape, pos=np.array([0, 0]), rot=0):
    """
    Returns the id of the (inside) node that reaches the
    lowest x-value
    """

    minimumX = None
    rightNodeID = None
    for node in shape.nodes:
        # If node isn't inside node
        if node.o != shape.o:
            continue

        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        if minimumX is None or nodePos[0] - node.r < minimumX:
            minimumX = nodePos[0] - node.r
            rightNodeID = node.ID

    return rightNodeID
