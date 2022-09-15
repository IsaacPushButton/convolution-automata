from dataclasses import dataclass

import shaders

WHITE = (1,1,1)
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)

class Preset:
    program: shaders.Shader
    vertex: shaders.Shader = shaders.Vertex()
    frag: shaders.Shader = shaders.Frag(*WHITE)

    def __init__(self, program: shaders.Shader):
        self.program = program

    def set_color(self, r: float, g: float, b: float, invert=False) -> 'Preset':
        self.frag = shaders.Frag(r, g, b, invert)
        return self


class Conway(Preset):
    program = shaders.Conway()

class Slime(Preset):
    program = shaders.Slime()

class Worms(Preset):
    program = shaders.Worm()

class WobblyWorms(Preset):
    program = shaders.custom_shader(
                convolve_vals=[
                    0.68, -0.8, 0.68,
                    -0.8, -0.66, -0.8,
                    0.68, -0.8, 0.68
                ],
                activation="-1./pow(2., (0.9*pow(x, 2.)))+1."
            )

class InkyCells(Preset):
    program = shaders.custom_shader(
                convolve_vals=shaders.symmetric_filter(.77, -0.85, -0.2),
                activation="-1./(0.89*pow(x, 2.)+1.)+1."
            )