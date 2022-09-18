from dataclasses import dataclass
from typing import List

import presets
import moderngl
import moderngl_window as mglw
from aenum import Enum, auto
import numpy as np

import shaders
import convolution_helper

BUTTON_MAPPING = {
    1 : 1.0,
    2 : 0.0
}
class Skip(Enum):
    Even = auto()
    Odd = auto()
    NoSkip = auto()
    Three = auto()

@dataclass
class GameConfig:
    window_size: (int, int)
    texture_size: (int, int)
    desired_fps: int
    skip: Skip
    preset: presets.Preset
    pause_start: bool

def print_filter(filter: List[float]):
    str_vals = [str(i) for i in filter]
    print("New filter:")
    print(",".join(str_vals[:3]))
    print(",".join(str_vals[3:6]))
    print(",".join(str_vals[6:]))
    print(f"Sum: {sum(filter)}")

def new_window(game_config: GameConfig):
    """Making class in a closure to pass values into it a bit easier"""
    class AutomataBase(mglw.WindowConfig):
        title = "Automata"
        window_size = game_config.window_size
        convolve_filter = None
        activation = None
        last_button = 0

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.paused = game_config.pause_start
            # How often the map should be updated
            self.update_delay = 1 / game_config.desired_fps  # updates per second
            self.last_updated = 0
            # size of the map
            self.width, self.height = game_config.texture_size
            # Force the window to calculate black borders if needed to retain the aspect ratio
            self.wnd.fixed_aspect_ratio = self.width / self.height
            self.even_frame = True
            # Initial state of the map (random)
            pixels = np.random.rand(self.width, self.height).astype('f4')

            # Program drawing the result to the screen.
            # This is rendered simply using a textured screen aligned triangle strip
            self.display_prog = self.ctx.program(
                vertex_shader=game_config.preset.vertex,
                fragment_shader=game_config.preset.frag,
            )

            # Program calculating the next state of the map
            self.transform_prog = self.ctx.program(
                vertex_shader=game_config.preset.program,
                varyings=['out_vert']
            )

            # Create the map texture
            self.texture = self.ctx.texture((self.width, self.height), 1, pixels.tobytes(), dtype='f4')
            self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
            self.texture.swizzle = 'RRR1'  # What components texelFetch will get from the texture (in shader)

            # A quad covering the screen with texture coordinates
            self.vbo = self.ctx.buffer(np.array([
                # x    y     u  v
                -1.0, -1.0, 0, 0,  # lower left
                -1.0, 1.0, 0, 1,  # upper left
                1.0, -1.0, 1, 0,  # lower right
                1.0, 1.0, 1, 1,  # upper right
            ], dtype="f4"))
            self.vao = self.ctx.simple_vertex_array(self.display_prog, self.vbo, 'in_vert', 'in_texcoord')
            # Transform vertex array to generate new map state
            self.tao = self.ctx.vertex_array(self.transform_prog, [])
            self.pbo = self.ctx.buffer(reserve=pixels.nbytes)  # buffer to store the result
            if game_config.skip == Skip.Odd:
                self.tao.transform(self.pbo, vertices=self.width * self.height)
                self.texture.write(self.pbo)

        def set_program(self, program: shaders.Shader):
            self.transform_prog = self.ctx.program(
                vertex_shader=program,
                varyings=['out_vert']
            )
            self.tao = self.ctx.vertex_array(self.transform_prog, [])

        def mouse_drag_event(self, x: int, y: int, dx: int, dy: int):
            self.mouse_press_event(x, y, self.last_button)

        def mouse_press_event(self, x: int, y: int, button: int):
            self.last_button = button
            buffer_vals = np.frombuffer(self.pbo.read(), dtype="f4").reshape(self.width, self.height)
            buffer_vals = buffer_vals.copy()
            ny = self.height - y
            for cell in convolution_helper.make_diamond_offset(55):
                buffer_vals[ny + cell[0], x + cell[1]] = convolution_helper.random_float(1)
            self.pbo.write(buffer_vals)
            self.texture.write(self.pbo)


        def key_event(self, key, action, modifiers):
            if action == self.wnd.keys.ACTION_PRESS and key == self.wnd.keys.SPACE:
                self.paused = not self.paused
            if action == self.wnd.keys.ACTION_PRESS and key == self.wnd.keys.C:
                new_filter = convolution_helper.random_symetric_small_bullseye(1)
                print_filter(new_filter.convolution_values)
                self.set_program(
                    shaders.custom_shader(
                        new_filter,
                        shaders.slime_activation()
                    )
                )
            if action == self.wnd.keys.ACTION_PRESS and key == self.wnd.keys.V:
                self.texture = self.ctx.texture((self.width, self.height), 1, np.random.rand(self.width, self.height).astype('f4').tobytes(), dtype='f4')
                self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
                self.texture.swizzle = 'RGB1'  # What components texelFetch will get from the texture (in shader)

            if action == self.wnd.keys.ACTION_PRESS and key == self.wnd.keys.B:
                self.texture = self.ctx.texture((self.width, self.height), 1, np.zeros((self.width, self.height),"f4").tobytes(), dtype='f4')
                self.texture.filter = moderngl.NEAREST, moderngl.NEAREST
                self.texture.swizzle = 'RGB1'  # What components texelFetch will get from the texture (in shader)

        def render(self, time, frame_time):
            self.ctx.clear(1.0, 1.0, 1.0)
            # Bind texture to channel 0
            self.texture.use(location=0)
            if time - self.last_updated > self.update_delay and not self.paused:
                # We cant actually skip anything, so we just run the transform
                # multiple times
                self.tao.transform(self.pbo, vertices=self.width * self.height)
                self.texture.write(self.pbo)
                if game_config.skip != Skip.NoSkip:
                    self.tao.transform(self.pbo, vertices=self.width * self.height)
                    self.texture.write(self.pbo)
                if game_config.skip == Skip.Three:
                    self.tao.transform(self.pbo, vertices=self.width * self.height)
                    self.texture.write(self.pbo)



                self.last_updated = time

            self.vao.render(moderngl.TRIANGLE_STRIP)
    return AutomataBase


