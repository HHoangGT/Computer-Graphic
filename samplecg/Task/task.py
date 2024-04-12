import numpy as np


def task1():
    # create 3 points of triangle randomly in 600x600 space
    points = np.random.randint(0, 600, (3, 2))
    # create randon point in the triangle
    p = np.random.randint(0, 600, (1, 2))
    # calculate the area of the triangle
    A = points[0, 0]
