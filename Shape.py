import numpy as np


class Node:
    def __init__(self, pos, radius, orientation, ID):
        # X and Y position on center
        self.pos = np.array(pos)
        # Radius
        self.r = radius
        # Orientation (+1 or -1) denotes which way around the boundry goes
        self.o = orientation
        self.ID = ID


class Shape:
    def __init__(self, nodes):
        self.nodes = nodes
        self.find_node_angles()
        self.calculateBindingLines()
        self.calculateOrientation()

    def find_node_angles(self):
        # Sets self.nodeAngles such that self.nodeAngles[ID] is a tuple
        # of the angle from the x axis that the point at which the
        # (incomming, outgoing) line touches the node

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

            # Update nodeAngles
            if node1.ID in self.nodeAngles:
                self.nodeAngles[node1.ID][1] = alpha
            else:
                self.nodeAngles[node1.ID] = [None, alpha]

            if node2.ID in self.nodeAngles:
                self.nodeAngles[node2.ID][0] = beta
            else:
                self.nodeAngles[node2.ID] = [beta, None]

    def calculateBindingLines(self):
        self.lines = []
        N = len(self.nodes)
        for nodeIndex in range(N):
            node1 = self.nodes[nodeIndex]
            node2 = self.nodes[(nodeIndex+1) % N]

            alpha = self.nodeAngles[node1.ID][1]
            beta = self.nodeAngles[node2.ID][0]

            linePoint1 = node1.pos + node1.r*np.array([np.cos(alpha), np.sin(alpha)])
            linePoint2 = node2.pos + node2.r*np.array([np.cos(beta), np.sin(beta)])

            self.lines.append(np.array([linePoint1, linePoint2]))


    def calculateOrientation(self):
        # Set self.positive orientation to true if the shape is 
        # positively oriented, that is, if the total angle change 
        # by the nodes is positive. 
        # If the shape is positively oriented, ALL nodes with positive
        # orientation are inside the shape and ALL nodes with negative
        # orientation are outside. 
        cumulative_angle_change = 0
        for node in self.nodes:
            # Calculate the angle change due to node
            angleIn, angleOut = self.nodeAngles[node.ID]
            angleChange = (angleOut - angleIn) % (2 * np.pi)
            print(angleChange *180/np.pi)
            if node.o == 1:
                cumulative_angle_change += angleChange
            elif node.o == -1:
                cumulative_angle_change -= (2*np.pi - angleChange)

        print(cumulative_angle_change * 180/np.pi)
        self.positive_orientation = cumulative_angle_change > 0


    #def calculateArea(self):
