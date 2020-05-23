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

    for node in shape.nodes:
        # if node is outside shape, continue
        if not node.o == shape.o:
            continue
        if (np.matmul(rotMat(rot), node.pos) + pos)[1] - node.r < -0.5:
            return False

    # No node (after trasposition and rotation) was below -0.5
    return True


def isInBounds(shape, pos, rot):
    "Returns True if no part of shape is outside of corridor"

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
            if segmentIntersectsArc(innerLine, nodePos, node.r,
                                    shape.nodeAngles[node.ID] + rot, node.o):
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

    for node in shape.nodes:
        # If node is not an inside node, continue
        if node.o != shape.o:
            continue

        nodePos = np.matmul(rotMat(rot), node.pos) + pos

        if nodePos[1] + node.r > 0.5 + tol:
            rvList.append([node.ID, 1])
        if nodePos[0] - node.r < -0.5 - tol:
            rvList.append([node.ID, 3])
        if nodePos[0] - node.r < -0.5 - tol and \
                nodePos[1] + node.r > 0.5 + tol:
            rvList.append([node.ID, 2])
        if nodePos[0] + node.r > 0.5 + tol and nodePos[1] <= -0.5:
            rvList.append([node.ID, 4])
        elif nodePos[1] - node.r < -0.5 - tol and nodePos[0] >= 0.5:
            rvList.append([node.ID, 4])
        elif np.linalg.norm(nodePos - np.array([0.5, -0.5])) < node.r + tol:
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
    origNodePos = np.matmul(rotMat(currentRot), shape.getNodeById(nodeID).pos)
    newNodePos = np.matmul(rotMat(theta), origNodePos)
    deltaPos = origNodePos - newNodePos
    return (deltaPos, deltaRot)


def shapeIsValid(shape):
    """
    Returns true if shape can be moved through a corridor with
    width 1 and a 90 degree turn to the right
    The corridor is initially centered on 0
    """

    topNode = shape.getNodeById(getTopNodeId(shape))
    maximumY = topNode.pos[1] + topNode.r
    rightNode = shape.getNodeById(getRightNodeId(shape))
    minimumX = rightNode.pos[0] - topNode.r

    # Place shape as far up and as far left as possible
    pos = [-0.5 - minimumX, 0.5 - maximumY]
    rot = 0

    # Check that it is in bounds to begin with
    if not isInBounds(shape, pos, rot):
        return False

    while True:
        deltaPosRot = posRotToShiftRightWithRot(shape, pos, rot)

        if deltaPosRot is None:
            return False
        else:
            pos += deltaPosRot[0]
            rot += deltaPosRot[1]

        if isThrough(shape, pos, rot):
            return True


def getWalk(shape):
    """
    Returns a sequence of positions and rotations that will get
    the shape through a corrodor with
    width 1 and a 90 degree turn to the right
    The corridor is centered on 0
    """

    topNode = shape.getNodeById(getTopNodeId(shape))
    maximumY = topNode.pos[1] + topNode.r
    rightNode = shape.getNodeById(getRightNodeId(shape))
    minimumX = rightNode.pos[0] - topNode.r

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
        # print(deltaPosRot)

        if deltaPosRot is None:
            return (poss, rots)
        else:
            pos += deltaPosRot[0]
            rot += deltaPosRot[1]
            poss.append(pos.copy())
            rots.append(rot)

        if isThrough(shape, pos, rot):
            return (poss, rots)


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
