from LineMath import linesIntersect
import numpy as np
import matplotlib.pyplot as plt

line1 = np.array([[0,0],[0,1]])
line2 = np.array([[-1,0.5],[1,0.5]])
print(f"Should be true; is: {linesIntersect(line1, line2)}")

line1 = np.array([[0,0],[0,1]])
line2 = np.array([[0,1],[1,1]])
print(f"Should be true; is: {linesIntersect(line1, line2)}")

line1 = np.array([[0,0],[0,1]])
line2 = np.array([[2,1],[3,1]])
print(f"Should be false; is: {linesIntersect(line1, line2)}")

line1 = np.array([[0,0],[0,1]])
line2 = np.array([[1,1],[-1,1]])
print(f"Should be true; is: {linesIntersect(line1, line2)}")

line1 = np.array([[0,0],[1,1]])
line2 = np.array([[0,1],[1,0]])
print(f"Should be true; is: {linesIntersect(line1, line2)}")


fig = plt.figure(1)
ax = fig.add_subplot()
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_title("Mark four points, if lines are red, linesIntersect")

while True:
    points = plt.ginput(4)
    line1 = np.array([points[0], points[1]])
    line2 = np.array([points[2], points[3]])

    col = "r" if linesIntersect(line1, line2) else "k"
    ax.plot(line1[:,0], line1[:,1], col)
    ax.plot(line2[:,0], line2[:,1], col)

    plt.draw()

