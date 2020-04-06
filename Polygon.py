import numpy as np


class Polygon:
    def __init__(self, xlist, ylist):
        self.xs = np.array(xlist)
        self.ys = np.array(ylist)

    def rotate(self, center, theta):
        # Rotate all points theta (float) radians around center (tuple)
        c, s = np.cos(theta), np.sin(theta)
        rotMatrix = np.array([[c, -s], [s, c]])
        self.xs, self.ys = np.matmul(rotMatrix, np.array([self.xs, self.ys]))

    def translate(self, vector):
        # Translate all points with vector
        self.xs = self.xs + vector[0]
        self.ys = self.ys + vector[1]
