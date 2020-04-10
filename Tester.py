import numpy as np
from copy import deepcopy


def isThrough(p):
    return all(p.ys >= 0)


dTheta = 0.2

def scooch(p, next_point):
    # Move p small amount so that the next point is at corner
    # Returns true if operation has been done and
    # false if it cannot be done

    # Translate shape
    moveBy = np.array([0-p.xs[next_point], 0-p.ys[next_point]])
    p.translate(moveBy)

    # Check if there are any points out of bounds,
    # If not, we're good to go
    if not (any(np.logical_and(p.xs > 0, p.ys < 0)) or any(p.ys > 1)):
        return True

    # Translate back, return false
    p.translate(-moveBy)
    return False


def moveSequence(p, seq=[], depth=0):
    # Returns a sequence of pxs and pys that navigates p through the corridor if posible, otherwise returns None
    # p - polygon, seq - sequence so far as [(p1.xs, p1.ys),(p2.xs ...

    if isThrough(p):
        return seq

    # Try to scootch
    tmP = deepcopy(p)
    scooched = scooch(tmP, depth)

    # If scooched, go deeper
    if scooched:
        newSeq = list(seq) + [(tmP.xs, tmP.ys)]
        while True:
            rv = moveSequence(tmP, newSeq, depth+1)
            # If rv isn't none, moveSequence returned a valid sequence
            if rv != None:
                return rv
            # Otherwise, there is no valid sequence. 
            # Rotate and try again
            tmP.rotate((0, 0), -dTheta)
            newSeq = newSeq + [(tmP.xs, tmP.ys)]
            # If there are points out of bounds after rot, there is no 
            # valid sequence
            if (any(np.logical_and(tmP.xs > 0, tmP.ys < 0)) or any(tmP.ys > 1) or any(tmP.xs < -1)):
                return None
            # Else, run again
    else:  # If not scooched, there is no valid sequence, return none
        return None

