import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Define the vertices of the cube
vertices = (
    (1, 1, 1),  # Top-right front
    (-1, 1, 1),  # Top-left front
    (-1, -1, 1),  # Bottom-left front
    (1, -1, 1),  # Bottom-right front
    (1, 1, -1),  # Top-right back
    (-1, 1, -1),  # Top-left back
    (-1, -1, -1),  # Bottom-left back
    (1, -1, -1),  # Bottom-right back
)

# Define the indices to connect the vertices into triangles
indices = (
    # Front face
    0, 1, 2, 2, 3, 0,
    # Back face
    4, 5, 6, 6, 7, 4,
    # Right face
    0, 3, 4, 4, 5, 1,
    # Left face
    6, 2, 1, 1, 5, 7,
    # Top face
    0, 4, 5, 5, 1, 0,
    # Bottom face
    2, 6, 7, 7, 3, 2,
)


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glRotatef(1, 1, 1, 0)  # Rotate the cube slightly each frame

    # Enable depth testing to hide occluded faces
    glEnable(GL_DEPTH_TEST)

    # Draw the cube using triangles
    glBegin(GL_TRIANGLES)
    for index in indices:
        glVertex3fv(vertices[index])
    glEnd()

    glutSwapBuffers()


def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(100, 100)
    glutCreateWindow("3D Cube")
    glutDisplayFunc(display)
    glutIdleFunc(display)  # Continuously redraw the scene
    glutMainLoop()


if __name__ == "__main__":
    main()
