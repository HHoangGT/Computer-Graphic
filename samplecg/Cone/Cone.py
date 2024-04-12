from libs.shader import *
from libs import transform as T
from libs.buffer import *
import ctypes
import glfw
import numpy as np


def cone(r, h, sides):
    vertices, indices, color, triangles = [], [], [], []

    # Calculating the vertices
    sideList = np.arange(0, sides, 1)
    thetaList = 2 * np.pi * sideList / sides
    xList = r * np.cos(thetaList)
    zList = r * np.sin(thetaList)
    for i in range(len(thetaList)):
        vertices.append([xList[i], -h / 2, zList[i]])
        color.append([0, 0, 1])

    # Calculating index list for the sides
    vertices.append([0, h / 2, 0])
    color.append([1, 0, 0])
    for i in range(sides):
        k1 = i
        k2 = k1 + 1
        if i != sides - 1:
            indices += [k1, len(vertices) - 1, k2]
            triangles += [[k1, len(vertices) - 1, k2]]
        else:
            indices += [k1, len(vertices) - 1, 0]
            triangles += [[k1, len(vertices) - 1, 0]]

    # Bottom
    vertices.append([0, -h / 2, 0])
    color.append([0, 1, 0])
    for i in range(sides):
        k1 = i
        k2 = k1 + 1
        if i != sides - 1:
            indices += [k1, len(vertices) - 1, k2]
            triangles += [[k1, len(vertices) - 1, k2]]
        else:
            indices += [k1, len(vertices) - 1, 0]
            triangles += [[k1, len(vertices) - 1, 0]]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    color = np.array(color, dtype=np.float32)

    # Calculating vertex normals
    def surfaceNormal(A, B, C):
        AB = B - A
        AC = C - A
        res = np.cross(AB, AC)
        return res

    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    vertexNormals = np.zeros((len(vertices), 3))

    for i in triangles:
        surfaceNormals = surfaceNormal(vertices[i[0]], vertices[i[1]], vertices[i[2]])
        vertexNormals[i[0]] += surfaceNormals
        vertexNormals[i[1]] += surfaceNormals
        vertexNormals[i[2]] += surfaceNormals
    vertexNormals = list(map(lambda x: normalize(x), vertexNormals))
    normals = np.array(vertexNormals, dtype=np.float32)

    return vertices, indices, color, normals


def cone_2(r, h, sides):
    vertices, indices, color, triangles = [], [], [], []

    # Calculating the vertices
    theta_step = 2 * np.pi / sides
    for i in range(sides):
        theta = i * theta_step
        x = r * np.cos(theta)
        z = r * np.sin(theta)
        vertices.append([x, -h / 2, z])
        color.append([0, 0, 1])

    # Apex vertex
    vertices.append([0, h / 2, 0])
    color.append([1, 0, 0])

    # Generate indices for triangle fan
    for i in range(sides):
        indices.extend([i, len(vertices) - 1, (i + 1) % sides])

    # Bottom
    bottom_center_index = len(vertices)
    vertices.append([0, -h / 2, 0])
    color.append([0, 1, 0])

    for i in range(sides):
        theta = i * theta_step
        x = r * np.cos(theta)
        z = r * np.sin(theta)
        vertices.append([x, -h / 2, z])
        color.append([0, 1, 0])
        indices.extend([bottom_center_index, len(vertices) - 1, bottom_center_index + ((i + 1) % sides)])

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    color = np.array(color, dtype=np.float32)

    # Calculating vertex normals
    def surfaceNormal(A, B, C):
        AB = B - A
        AC = C - A
        res = np.cross(AB, AC)
        return res

    def normalize(v):
        norm = np.linalg.norm(v)
        if norm == 0:
            return v
        return v / norm

    vertexNormals = np.zeros((len(vertices), 3))

    for i in range(len(indices) // 3):
        i1, i2, i3 = indices[i * 3], indices[i * 3 + 1], indices[i * 3 + 2]
        surfaceNormals = surfaceNormal(vertices[i1], vertices[i2], vertices[i3])
        vertexNormals[i1] += surfaceNormals
        vertexNormals[i2] += surfaceNormals
        vertexNormals[i3] += surfaceNormals

    vertexNormals = list(map(lambda x: normalize(x), vertexNormals))
    normals = np.array(vertexNormals, dtype=np.float32)

    return vertices, indices, color, normals


class Cone(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices, self.indices, self.colors, self.normals = cone(0.5, 1, 20)

        self.vao = VAO()

        self.shader = Shader(vert_shader, frag_shader)
        self.uma = UManager(self.shader)
        #

    """
    Create object -> call setup -> call draw
    """

    def setup(self):
        # setup VAO for drawing cylinder's side
        self.vao.add_vbo(0, self.vertices, ncomponents=3, stride=0, offset=None)
        self.vao.add_vbo(1, self.colors, ncomponents=3, stride=0, offset=None)

        # setup EBO for drawing cylinder's side, bottom and top
        self.vao.add_ebo(self.indices)

        return self

    def draw(self, projection, view, model):
        GL.glUseProgram(self.shader.render_idx)
        modelview = view

        self.uma.upload_uniform_matrix4fv(projection, 'projection', True)
        self.uma.upload_uniform_matrix4fv(modelview, 'modelview', True)

        self.vao.activate()
        GL.glDrawElements(GL.GL_TRIANGLE_STRIP, self.indices.shape[0], GL.GL_UNSIGNED_INT, None)

    def key_handler(self, key):

        if key == glfw.KEY_1:
            self.selected_texture = 1
        if key == glfw.KEY_2:
            self.selected_texture = 2
