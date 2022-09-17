from dataclasses import dataclass
from typing import TypeVar, Tuple

import shaders

Colour = TypeVar("Colour", bound=Tuple[float, float, float])
WHITE = (1, 1, 1)
RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)


class Preset:
    program: shaders.Shader
    colour: Colour
    vertex: shaders.Shader = shaders.Vertex()

    def __init__(self, program: shaders.Shader, colour: Colour = (1, 1, 1)):
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
    program=shaders.custom_shader(
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
    program=shaders.custom_shader(
        convolve_vals=shaders.symmetric_filter(.77, -0.85, -0.2),
        activation="-1./(0.89*pow(x, 2.)+1.)+1."
    )
)

Fireballs = Preset(
    program=shaders.custom_shader(
        convolve_vals=shaders.symmetric_filter(-1.3391863202051066, 1.555111014243741, -0.916115840759975),
        activation=shaders.slime_activation()
    )
)

FuzzyToplogy = Preset(
    program=shaders.custom_shader(
        convolve_vals=shaders.symmetric_filter(1.7202596155940522, -1.95276936614261, 1.51132282843589),
        activation=shaders.slime_activation()
    )
)

ScrollingBars = Preset(
    program=shaders.custom_shader(
        convolve_vals=[-0.7637923023208057, 0.1371390959408756, 0.5766589520075494,
                       -0.7792009602667, 0.9769278653658324, 0.6470866205481296,
                       -0.8213450225834913, 0.17574366282070697, 0.4018650187180264],
        activation=shaders.slime_activation()
    )
)

Fabric = Preset(
    program=shaders.custom_shader(
        convolve_vals=[-0.31248013131115226, 0.6845770547395884, -0.005333066652860152,
                       -0.36197855073992735, -0.8494108908372158, 0.13892485834787904,
                       0.3443299042015695, -0.7536027887557468, -0.9211287992570929],
        activation=shaders.slime_activation()
    )
)
