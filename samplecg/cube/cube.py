from libs.shader import *
from libs import transform as T
from libs.buffer import *
import ctypes
import glfw


class Cube(object):
    def __init__(self, vert_shader, frag_shader):
        self.vertices = np.array(
            [
                [-1, -1, +1],  # A <= Bottom: ABCD
                [+1, -1, +1],  # B
                [+1, -1, -1],  # C
                [-1, -1, -1],  # D
                [-1, +1, +1],  # E <= Top: EFGH
                [+1, +1, +1],  # F
                [+1, +1, -1],  # G
                [-1, +1, -1],  # H
            ],
            dtype=np.float32
        )

        self.indices = np.array(
            [0, 4, 1, 5, 2, 6, 3, 7, 0, 4, 4, 0, 0, 3, 1, 2, 2, 4, 4, 7, 5, 6],
            dtype=np.int32
        )

        self.normals = self.vertices.copy()
        self.normals = self.normals / np.linalg.norm(self.normals, axis=1, keepdims=True)

        # colors: RGB format
        self.colors = np.array(
            [  # R    G    B
                [1.0, 0.0, 0.0],  # A <= Bottom: ABCD
                [1.0, 0.0, 1.0],  # B
                [0.0, 0.0, 1.0],  # C
                [0.0, 0.0, 0.0],  # D
                [1.0, 1.0, 0.0],  # E <= Top: EFGH
                [1.0, 1.0, 1.0],  # F
                [0.0, 1.0, 1.0],  # G
                [0.0, 1.0, 0.0],  # H
            ],
            dtype=np.float32
        )

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

