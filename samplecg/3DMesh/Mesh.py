import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy as np


def f(x, z):
    """
    Function representing the surface to be visualized.
    """
    return x ** 4 - 2 * x ** 2 + z ** 2


def generate_vertices(resolution=20):
    """
    Generates vertices for the mesh based on the provided function and resolution.
    """
    x, z = np.linspace(-2, 2, resolution + 1), np.linspace(-2, 2, resolution + 1)
    X, Z = np.meshgrid(x, z)
    Y = f(X, Z)
    vertices = np.dstack((X, Y, Z)).reshape(-1, 3)
    return vertices


def display(resolution=20):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1, 1, 0, 0)  # Rotate the mesh slightly for better observation

    # Enable depth testing to hide occluded faces
    glEnable(GL_DEPTH_TEST)

    glBegin(GL_QUADS)
    for i in range(resolution):
        for j in range(resolution):
            # Define quad based on grid indices
            index = i * (resolution + 1) + j
            glVertex3fv(vertices[index])
            glVertex3fv(vertices[index + 1])
            glVertex3fv(vertices[index + resolution + 2])
            glVertex3fv(vertices[index + resolution + 1])
    glEnd()

    glutSwapBuffers()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("3D Mesh")
    glutDisplayFunc(display)
    glutIdleFunc(display)  # Continuously redraw the scene
    glutMainLoop()


if __name__ == "__main__":
    vertices = generate_vertices()
    main()
