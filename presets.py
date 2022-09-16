from dataclasses import dataclass
from typing import TypeVar, Tuple

import shaders

Colour = TypeVar("Colour", bound=Tuple[float,float,float])
WHITE = (1,1,1)
RED = (1,0,0)
GREEN = (0,1,0)
BLUE = (0,0,1)

class Preset:
    program: shaders.Shader
    colour: Colour
    vertex: shaders.Shader = shaders.Vertex()

    def __init__(self, program: shaders.Shader, colour: Colour = (1,1,1)):
        self.program = program
        self.colour = colour
        self.frag: shaders.Shader = shaders.Frag(*self.colour)


Conway = Preset(
    program=shaders.Conway(),
    colour=GREEN
)

Slime = Preset(
    program=shaders.Slime(),
    colour=GREEN
)

Worms = Preset(
    program=shaders.Worm(),
    colour=RED
)

WobblyWorms = Preset(
    program = shaders.custom_shader(
                convolve_vals=[
                    0.68, -0.8, 0.68,
                    -0.8, -0.66, -0.8,
                    0.68, -0.8, 0.68
                ],
                activation="-1./pow(2., (0.9*pow(x, 2.)))+1."
            ),
    colour=BLUE
)

InkyCells = Preset(
    program = shaders.custom_shader(
                convolve_vals=shaders.symmetric_filter(.77, -0.85, -0.2),
                activation="-1./(0.89*pow(x, 2.)+1.)+1."
            )
)