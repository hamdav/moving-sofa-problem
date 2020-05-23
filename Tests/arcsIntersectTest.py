import numpy as np
import matplotlib.pyplot as plt

from LineMath import arcsIntersect


def arc(center, radius, angle1, angle2, o):
    if o == -1:
        angle1, angle2 = angle2, angle1
    # Returns a list of xs and a list of ys that make up an arc.
    if angle2 < angle1:
        angle2 += 2*np.pi

    angles = np.linspace(angle1, angle2, 100)

    xs = center[0] + np.cos(angles) * radius
    ys = center[1] + np.sin(angles) * radius
    return (xs, ys)


print(" - - - Simple tests - - - ")
c1 = np.array([0, 0])
a1 = np.array([6, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([1.5, 0])
a2 = np.array([1, 6])
arc2 = [c2, 1, a2, 1]
print(f"Should be true, is {arcsIntersect(*arc1, *arc2)}")

c1 = np.array([0, 0])
a1 = np.array([6, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([1.5, 0])
a2 = np.array([6, 1])
arc2 = [c2, 1, a2, -1]
print(f"Should be true, is {arcsIntersect(*arc1, *arc2)}")

c1 = np.array([0, 0])
a1 = np.array([6, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([2.5, 0])
a2 = np.array([6, 1])
arc2 = [c2, 1, a2, -1]
print(f"Should be false, is {arcsIntersect(*arc1, *arc2)}")

c1 = np.array([0, 0])
a1 = np.array([6.1, 0.1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([1.5, 0])
a2 = np.array([6, 1])
arc2 = [c2, 1, a2, -1]
print(f"Should be false, is {arcsIntersect(*arc1, *arc2)}")

print(" - - - edge cases - - -")
c1 = np.array([0, 0])
a1 = np.array([6.1, 0.1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([2, 0])
a2 = np.array([6, 1])
arc2 = [c2, 1, a2, -1]
print(f"kissing arcs: Should be false, is {arcsIntersect(*arc1, *arc2)}")
c1 = np.array([0, 0])
a1 = np.array([0, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([0, 0])
a2 = np.array([1, 2])
arc2 = [c2, 1, a2, 1]
print(f"touching endpoints: Should be false, is {arcsIntersect(*arc1, *arc2)}")
c1 = np.array([0, 0])
a1 = np.array([0, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([0, 0])
a2 = np.array([0, 1])
arc2 = [c2, 1, a2, 1]
print(f"entirely overlapping: Should be false?, is {arcsIntersect(*arc1, *arc2)}")
c1 = np.array([0, 0])
a1 = np.array([0, 1])
arc1 = [c1, 1, a1, 1]
c2 = np.array([1, -1])
a2 = np.array([0, 3])
arc2 = [c2, 1, a2, 1]
print(f"endpoint touching middle: Should be false, is {arcsIntersect(*arc1, *arc2)}")

fig, ax = plt.subplots()
x, y = arc(c1, 1, *a1, 1)
ax.plot(x, y)
x, y = arc(c2, 1, *a2, 1)
ax.plot(x, y)

ax.set_xlim(0,3)
ax.set_ylim(-1,1)
plt.show()
