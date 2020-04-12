import numpy as np
import LineMath



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

        mutationProbabillity = 0.1
        mutationLength = 0.05
        n = len(self.xs)

        newXs = np.copy(self.xs)
        newYs = np.copy(self.ys)

        for pointIndex in range(n):
            # Decide whether to mutate or not
            if np.random.random() > mutationProbabillity:
                continue

            # Move the point a little bit TODO: Better movement
            oldPoint = np.array([self.xs[pointIndex], self.ys[pointIndex]])
            newPoint = oldPoint + (np.random.random(2)-0.5) * 2 * mutationLength

            # Check that this does not cross any other line
            # If not, mutation is valid
            mutationIsValid = True

            # Name line ending on new point and line beginning on new point
            # These should not cross any other line
            lineToMovedPoint   = (np.array([newXs[pointIndex-1],       newYs[pointIndex-1]]), newPoint)
            lineFromMovedPoint = (np.array([newXs[(pointIndex+1) % n], newYs[(pointIndex+1) % n]]), newPoint)

            # Line checked is the one from otherPointIndex to otherPointIndex - 1.
            for otherPointIndex in range(n):
                # If the line checked has moved point as endpoint, ignore.
                if otherPointIndex == pointIndex or (otherPointIndex - 1) % n == pointIndex:
                    continue

                # Create the line to be checked
                lineToCheckIfCrossed = np.array([np.array([newXs[otherPointIndex-1], newYs[otherPointIndex-1]]),
                                                 np.array([newXs[otherPointIndex], newYs[otherPointIndex]])])

                # if (not LineMath.boxesIntersect(lineToMovedPoint, lineToCheckIfCrossed)) and (not LineMath.boxesIntersect(lineFromMovedPoint, lineToCheckIfCrossed)):
                    #continue

                # If you got here, they are close. 
                # Check if the lines intersect, if so, break out of the for otherpoint
                # If the line to check borders one of the lines from or to the point moved,
                # don't check if they intersect, cause they will

                # If line borders line to point
                if otherPointIndex == ((pointIndex -1) % n):
                    if LineMath.linesIntersect(lineFromMovedPoint, lineToCheckIfCrossed):
                        mutationIsValid = False
                        break
                # If line borders line from point
                elif ((otherPointIndex - 1) % n) == ((pointIndex +1) % n):
                    if LineMath.linesIntersect(lineToMovedPoint, lineToCheckIfCrossed):
                        mutationIsValid = False
                        break
                else:
                    if LineMath.linesIntersect(lineToMovedPoint, lineToCheckIfCrossed) or LineMath.linesIntersect(lineFromMovedPoint, lineToCheckIfCrossed):
                        mutationIsValid = False
                        break


            if mutationIsValid:
                newXs[pointIndex] = newPoint[0]
                newYs[pointIndex] = newPoint[1]

        return Polygon(newXs, newYs)

