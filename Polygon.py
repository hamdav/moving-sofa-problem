import numpy as np


class Polygon:
    def __init__(self, xlist, ylist):
        # coordinates are shifted such that the first one is at 0,0
        self.xs = np.array(xlist) - xlist[0]
        self.ys = np.array(ylist) - ylist[0]
        self.calculateArea()

    def rotate(self, center, theta):
        # Rotate all points theta (float) radians around center (tuple)
        c, s = np.cos(theta), np.sin(theta)
        rotMatrix = np.array([[c, -s], [s, c]])
        self.xs, self.ys = np.matmul(rotMatrix, np.array([self.xs, self.ys]))

    def translate(self, vector):
        # Translate all points with vector
        self.xs = self.xs + vector[0]
        self.ys = self.ys + vector[1]

    def calculateArea(self):
        n = len(self.xs)
        area = 0.0
        for i in range(n):
            j = (i + 1) % n
            area += self.xs[i] * self.ys[j]
            area -= self.xs[j] * self.ys[i]
        self.area = abs(area) / 2.0

    # Simple random choice = 16.7 s for 100 000 offsprings
    def createOffspring(self):
        newXs = self.xs + np.random.random(len(self.xs))/100
        newYs = self.ys + np.random.random(len(self.ys))/100
        return Polygon(newXs, newYs)
