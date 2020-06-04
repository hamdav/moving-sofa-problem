import numpy as np
from copy import deepcopy
import itertools

from LineMath import linesIntersect
from LineMath import segmentIntersectsArc
from LineMath import arcsIntersect


class Node:
    def __init__(self, pos, radius, orientation, ID=0):
        # X and Y position on center
        self.pos = np.array(pos)
        # Radius
        self.r = radius
        # Orientation (+1 or -1) denotes which way around the boundry goes
        self.o = orientation
        self.ID = ID


class Shape:
    """
    The shape class consists of nodes with orientations.
    These are bound together with lines
    The class always contains the following properties

    self.nodes: list of node objects

    self.nodeAngles: dictionare with node.ID as keys and
    np.array([angleIn, angleOut]) as values.
    The angles are the angles at which
    the incomming and outgoing lines touch the node,
    counted positively and from the x axis.
    Angles are always between 0 and 2 pi.

    self.o: 1 if orientation is positive, -1 if it is negative
    orientation is calculated from node angles, if the shape turns
    more in the positive direction, its positive and vice versa.

    self.lines: list of binding lines on the form
    np.array([[[x1,y1], [x2, y2]], [[x1, y1], [x2, y2]], ...])

    self.area: the area of the shape
    """

    def __init__(self, nodes):
        self.nodes = nodes
        self.recalculate()

    def recalculate(self):
        """"
        Recalculates nodeAngles, binding lines, orientation, area and nodeIDs
        WARNING! Never recalculate a shape that has already been out
        in the world. The switching of nodeIDs may cause probelms.
        Recalculate is simply meant to be done at creation to make shape correct.
        """

        ID = 0
        for node in self.nodes:
            node.ID = ID
            ID += 1

        # Check that calculating stuff is even possible
        if not self.nodePositionsIsValid():
            self.valid = False
            return

        self.findNodeAngles()
        self.calculateBindingLines()
        self.calculateOrientation()
        self.calculateArea()

        # If it isn't simple, it isn't valid
        self.valid = self.isSimple()

    def mutateInPlace(self, bigMutations=False):
        """
        Returns a mutated copy of shape.

        If bigMutations is True, number of nodes
        and orientation can be changed
        otherwise, it's just node pos and radii that can change
        Mutations are normally distributed with mean 0 and
        """

        # Set probabillities
        mutatePosProb = 1.0/len(self.nodes)
        mutateRadProb = 1.0/len(self.nodes)
        mutateNoProb = 0.1
        mutateOrProb = 0.1

        # Set rates
        posStd = 0.05
        radStd = 0.02

        for node in self.nodes:
            # With probabillity mutatePosProb, mutate position
            if np.random.random_sample() < mutatePosProb:
                deltaPos = np.random.normal(0, posStd, 2)
                node.pos += deltaPos
                # Check that this mutation didn't make it not simple
                self.recalculate()
                if not self.valid:
                    # If it did, undo it
                    node.pos -= deltaPos
                    self.recalculate()

            # With probabillity mutateRadProb, mutate radius
            if np.random.random_sample() < mutateRadProb:
                deltaRad = np.random.normal(0, radStd)
                # The radius cannot be 0 or negative
                if node.r + deltaRad <= 0:
                    continue
                node.r += deltaRad
                # Check that this mutation didn't make it not simple
                self.recalculate()
                if not self.valid:
                    # If it did, undo it
                    node.r -= deltaRad
                    self.recalculate()

        if bigMutations:
            # with probabillity mutateNoProb, add a node between two nodes
            if np.random.random_sample() < mutateNoProb:
                # NodeID for node before which to insert new node
                nodeID = np.random.choice(len(self.nodes))
                newNodePos = (self.nodes[nodeID].pos + self.nodes[nodeID-1].pos)/2.0
                # r is at least 0.01 and expected around 0.1
                newNodeR = np.abs(np.random.normal(0.1,0.05)) + 0.01
                newNodeO = np.random.choice([-1,1])
                newNode = Node(newNodePos, newNodeR, newNodeO, nodeID)
                self.nodes.insert(nodeID, newNode)

                # Check that shape is still valid
                self.recalculate()
                if not self.valid:
                    del self.nodes[nodeID]
                    self.recalculate()

            # With probabillity mutateNoProb, remove a node
            if np.random.random_sample() < mutateNoProb and len(self.nodes) >= 3:
                # NodeID for node to remove
                nodeID = np.random.choice(len(self.nodes))
                removedNode = self.nodes[nodeID]
                del self.nodes[nodeID]
                # Check that shape is still valid
                self.recalculate()
                if not self.valid:
                    self.nodes.insert(nodeID, removedNode)
                    self.recalculate()

            # With probabillity mutateOrProb, change a nodes orientation
            if np.random.random_sample() < mutateOrProb:
                nodeID = np.random.choice(len(self.nodes))
                self.nodes[nodeID].o *= -1
                # Check that shape is still valid
                self.recalculate()
                if not self.valid:
                    self.nodes[nodeID].o *= -1
                    self.recalculate()

    def nodePositionsIsValid(self):
        """"
        Checks the simple validity of shape

        Just checks that no nodes are too close to each other
        to even construct the binding lines.
        """

        # No consecutive nodes can be inside each other
        # No consecutive nodes of opposite orientation 
        # can intersect
        for nodeIndex in range(len(self.nodes)):
            node1 = self.nodes[nodeIndex]
            node2 = self.nodes[nodeIndex-1]
            dist = np.linalg.norm(node1.pos - node2.pos)
            if dist + node1.r < node2.r:
                return False
            if dist + node2.r < node1.r:
                return False
            if node1.o != node2.o:
                # They cannot intersect
                if dist < node1.r + node2.r:
                    return False
        return True

    def isSimple(self):
        "Checks that the shape is simple, if so, return True, else False"

        # Check that no two binding lines cross
        for line1, line2 in itertools.combinations(self.lines, 2):
            if linesIntersect(line1, line2):
                return False

        # Check that no arc intersects a binding line
        for node in self.nodes:
            for line in self.lines:
                if segmentIntersectsArc(line, node.pos, node.r,
                                        self.nodeAngles[node.ID], node.o):
                    return False

        # Check that no two arcs intersect each other
        for node1, node2 in itertools.combinations(self.nodes, 2):
            if arcsIntersect(node1.pos, node1.r,
                             self.nodeAngles[node1.ID], node1.o,
                             node2.pos, node2.r,
                             self.nodeAngles[node2.ID], node2.o):
                return False

        return True

    def findNodeAngles(self):
        """
        Sets self.nodeAngles such that self.nodeAngles[ID] is a tuple
        of the angle from the x axis that the point at which the
        (incomming, outgoing) line touches the node
        """

        N = len(self.nodes)

        # Initialize nodeAngles as an empty dictionary
        self.nodeAngles = {}

        for nodeIndex in range(N):
            node1 = self.nodes[nodeIndex]
            node2 = self.nodes[(nodeIndex+1) % N]

            # Vector from center of 1 to center of 2
            vector12 = node2.pos - node1.pos
            dist12 = np.linalg.norm(vector12)

            # Angle vector makes with pos x axis, \in [-pi, pi]
            theta = np.arctan2(vector12[1], vector12[0])

            # Calculate angles (from vector12) where the line touches
            # If orientations are the same:
            if node1.o * node2.o == 1:
                alpha = np.arccos((node1.r - node2.r)/dist12)
                beta = alpha
            # If orientations are different:
            elif node1.o * node2.o == -1:
                alpha = np.arccos((node1.r + node2.r)/dist12)
                beta = alpha-np.pi

            # If node1s orientation is 1, flip the signs of the angles
            alpha *= -node1.o
            beta *= -node1.o

            # Add theta to the angles
            alpha += theta
            beta += theta

            # Make angles be between 0 and 2 pi
            alpha = alpha % (2*np.pi)
            beta = beta % (2*np.pi)

            #breakpoint()
            # Update nodeAngles
            if node1.ID in self.nodeAngles:
                self.nodeAngles[node1.ID][1] = alpha
            else:
                self.nodeAngles[node1.ID] = np.array([None, alpha])

            if node2.ID in self.nodeAngles:
                self.nodeAngles[node2.ID][0] = beta
            else:
                self.nodeAngles[node2.ID] = np.array([beta, None])

    def calculateBindingLines(self):
        N = len(self.nodes)
        self.lines = np.empty((N,2,2))
        #breakpoint()
        for nodeIndex in range(N):
            node1 = self.nodes[nodeIndex]
            node2 = self.nodes[(nodeIndex+1) % N]

            alpha = self.nodeAngles[node1.ID][1]
            beta = self.nodeAngles[node2.ID][0]

            linePoint1 = node1.pos + node1.r * \
                np.array([np.cos(alpha), np.sin(alpha)])
            linePoint2 = node2.pos + node2.r * \
                np.array([np.cos(beta), np.sin(beta)])

            self.lines[nodeIndex] = np.array([linePoint1, linePoint2])

    def calculateOrientation(self):
        """
        Set self.positive orientation to true if the shape is
        positively oriented, that is, if the total angle change
        by the nodes is positive.
        If the shape is positively oriented, ALL nodes with positive
        orientation are inside the shape and ALL nodes with negative
        orientation are outside.
        """

        cumulativeAngleChange = 0
        for node in self.nodes:
            # Calculate the angle change due to node
            angleIn, angleOut = self.nodeAngles[node.ID]
            # Angle change is out - in if positively oriented,
            # and in - out if negatively oriented
            angleChange = (node.o*(angleOut - angleIn)) % (2 * np.pi)
            if node.o == 1:
                cumulativeAngleChange += angleChange
            elif node.o == -1:
                cumulativeAngleChange -= angleChange

        self.o = 1 if cumulativeAngleChange > 0 else -1

    def calculateArea(self):
        """
        Calculates the area of the shape
        step one: calculate the area of the shape created by
        the binding lines and the centers of the nodes
        Then, add the circle sectors from the circles inside the shape
        and subtract the circle sectors on the outside.
        """

        # Create all of the points for the first shape
        # Also sum up the circle sector areas
        points = np.empty((0, 2), float)
        circleSectorAreas = 0
        for node in self.nodes:
            pos = node.pos
            angleIn, angleOut = self.nodeAngles[node.ID]
            deltap1 = node.r * np.array([np.cos(angleIn), np.sin(angleIn)])
            deltap2 = node.r * np.array([np.cos(angleOut), np.sin(angleOut)])

            points = np.vstack((points, pos + deltap1))
            points = np.vstack((points, pos))
            points = np.vstack((points, pos + deltap2))

            # Calculate and add the circle sector area
            # The angle change is out - in if positively oriented
            # but in - out if negatively oriented.
            deltaAngle = (node.o * (angleOut - angleIn)) % (2*np.pi)
            # Circle sector should be added if inside and subtracted if
            # outside
            circleSectorAreas += self.o * node.o * node.r**2 * deltaAngle / 2

        # Shift points so that first point is at 0,0
        points = points - points[0]

        # Calculate the area
        area = 0.0
        n = len(points)
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        area = abs(area) / 2.0

        # Add the circleSectorAreas
        self.area = area + circleSectorAreas

