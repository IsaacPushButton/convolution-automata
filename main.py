
import numpy as np

import moderngl
import moderngl_window as mglw
import shaders

PROG = shaders.worm

class Automata(mglw.WindowConfig):
    title = "Automata"
    window_size = 800, 800

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # How often the map should be updated
        self.update_delay = 1 / 500  # updates per second
        self.last_updated = 0
        # size of the map
        self.width, self.height = 600, 600
        # Force the window to calculate black borders if needed to retain the aspect ratio
        self.wnd.fixed_aspect_ratio = self.width / self.height
        self.even_frame = True
        # Initial state of the map (random)
        pixels = np.random.rand(self.width, self.height).astype('f4')

        # Program drawing the result to the screen.
        # This is rendered simply using a textured screen aligned triangle strip
        self.display_prog = self.ctx.program(
            vertex_shader=shaders.vertex,
            fragment_shader=shaders.frag,
        )

        # Program calculating the next state of the map
        self.transform_prog = self.ctx.program(
            vertex_shader=PROG,
            varyings=['out_vert']
        )

        # Create the map texture
        self.texture = self.ctx.texture((self.width, self.height), 1, pixels.tobytes(), dtype='f4')
        self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
        self.texture.swizzle = 'RRR1'  # What components texelFetch will get from the texture (in shader)

        # A quad covering the screen with texture coordinates
        self.vbo = self.ctx.buffer(np.array([
            # x    y     u  v
            -1.0, -1.0,  0, 0,  # lower left
            -1.0,  1.0,  0, 1,  # upper left
            1.0,  -1.0,  1, 0,  # lower right
            1.0,   1.0,  1, 1,  # upper right
        ], dtype="f4"))
        self.vao = self.ctx.simple_vertex_array(self.display_prog, self.vbo, 'in_vert', 'in_texcoord')
        # Transform vertex array to generate new map state
        self.tao = self.ctx.vertex_array(self.transform_prog, [])
        self.pbo = self.ctx.buffer(reserve=pixels.nbytes)  # buffer to store the result

    def render(self, time, frame_time):
        self.ctx.clear(1.0, 1.0, 1.0)
        # Bind texture to channel 0
        self.texture.use(location=0)
        if time - self.last_updated > self.update_delay:
            self.tao.transform(self.pbo, vertices=self.width * self.height)
            self.texture.write(self.pbo)
            self.tao.transform(self.pbo, vertices=self.width * self.height)
            self.texture.write(self.pbo)
            self.last_updated = time

        self.vao.render(moderngl.TRIANGLE_STRIP)




if __name__ == '__main__':
    Automata.run()