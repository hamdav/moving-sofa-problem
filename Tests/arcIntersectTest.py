import numpy as np
import matplotlib.pyplot as plt

from LineMath import segmentIntersectsArc


def arc(center, radius, angle1, angle2):
    # Returns a list of xs and a list of ys that make up an arc.
    if angle2 < angle1:
        angle2 += 2*np.pi

    angles = np.linspace(angle1, angle2, 100)

    xs = center[0] + np.cos(angles) * radius
    ys = center[1] + np.sin(angles) * radius
    return (xs, ys)


line1 = np.array([[-1, 1], [1, 1]])
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [0, 3.14])}")
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [0, 3.16])}")
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [6, 3.14])}")
line1 = np.array([[-1, 0.9], [1, 1.1]])
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [0, 3.14])}")
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [0, 3.16])}")
print(f"should be false, is {segmentIntersectsArc(line1, np.array([0,0]), 0.95, [6, 3.14])}")
line1 = np.array([[0,0],[0,1]])
print(f"should be true, is {segmentIntersectsArc(line1, np.array([0,0]), 0.9, [0, 3.14])}")
line1 = np.array([[0,0],[1,0]])
print(f"should be true, is {segmentIntersectsArc(line1, np.array([0,0]), 0.9, [6, 1])}")
line1 = np.array([[0,0],[1,-1]])
print(f"should be true, is {segmentIntersectsArc(line1, np.array([1,0]), 0.9, [1, 6])}")


fig = plt.figure(1)
ax = fig.add_subplot()
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.set_title("Mark five points, if lines are red, linesIntersect")

while True:
    points = plt.ginput(5, timeout=0)
    line1 = np.array([points[0], points[1]])
    radius = np.linalg.norm(np.array(points[3])-np.array(points[2]))
    angle1 = np.arctan2(points[3][1]-points[2][1],
                        points[3][0]-points[2][0]) % (2*np.pi)
    angle2 = np.arctan2(points[4][1]-points[2][1],
                        points[4][0]-points[2][0]) % (2*np.pi)
    arcPoints = arc(points[2], radius, angle1, angle2)

    col = "r" if segmentIntersectsArc(
        line1, points[2], radius, [angle1, angle2]) else "k"
    ax.plot(line1[:, 0], line1[:, 1], col)
    ax.plot(arcPoints[0], arcPoints[1], col)

    plt.draw()
