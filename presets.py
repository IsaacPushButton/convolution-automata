from dataclasses import dataclass
from typing import TypeVar, Tuple
import convolution_helper
import shaders
from convolution_helper import build_filter

Colour = TypeVar("Colour", bound=Tuple[float, float, float])
WHITE = (1, 1, 1)

RED = (1, 0, 0)
GREEN = (0, 1, 0)
BLUE = (0, 0, 1)

PINK = (1, 0.5, 0.5)


class Preset:
    program: shaders.Shader
    colour: Colour
    vertex: shaders.Shader = shaders.Vertex()

    def __init__(self, program: shaders.Shader, colour: Colour = (1, 1, 1)):
        self.program = program
        self.colour = colour
        self.frag: shaders.Shader = shaders.Frag()



convolution_filter_r = convolution_helper.symmetric_filter_3x3(0.2781675312739802, -0.9434019420809658, -0.9434019420809658)
convolution_filter_g = convolution_helper.symmetric_filter_medium_circle(-1.3391863202051066, 1.555111014243741,-0.916115840759975, 0.1)
convolution_filter_b = convolution_helper.symmetric_filter_3x3(0.2781675312739802, -0.9434019420809658, -0.9434019420809658)

MulipleNeighbours = Preset(
    program=shaders.custom_shader(
        convolution_filters=[convolution_filter_r, convolution_helper.Convolution_Filter(convolution_values=[0], convolution_offsets=[(0,0)]), convolution_helper.Convolution_Filter(convolution_values=[0], convolution_offsets=[(0,0)])],
        activation=shaders.worm_activation()
    ),
)

