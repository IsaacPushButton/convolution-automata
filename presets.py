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
        convolution_filter=build_filter([
            0.68, -0.8, 0.68,
            -0.8, -0.66, -0.8,
            0.68, -0.8, 0.68
        ]),
        activation="-1./pow(2., (0.9*pow(x, 2.)))+1."
    ),
    colour=BLUE
)

InkyCells = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.symmetric_filter_3x3(.77, -0.85, -0.2),
        activation="-1./(0.89*pow(x, 2.)+1.)+1."
    )
)

Fireballs = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.symmetric_filter_3x3(-1.3391863202051066, 1.555111014243741,
                                                                   -0.916115840759975),
        activation=shaders.slime_activation()
    )
)

FuzzyToplogy = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.symmetric_filter_3x3(1.7202596155940522, -1.95276936614261,
                                                                   1.51132282843589),
        activation=shaders.slime_activation()
    )
)

ScrollingBars = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([-0.7637923023208057, 0.1371390959408756, 0.5766589520075494,
                                                            -0.7792009602667, 0.9769278653658324, 0.6470866205481296,
                                                            -0.8213450225834913, 0.17574366282070697,
                                                            0.4018650187180264]),
        activation=shaders.slime_activation()
    )
)

Fabric = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter(
            [-0.31248013131115226, 0.6845770547395884, -0.005333066652860152,
             -0.36197855073992735, -0.8494108908372158, 0.13892485834787904,
             0.3443299042015695, -0.7536027887557468, -0.9211287992570929]),
        activation=shaders.slime_activation()
    )
)

SlowJoiningBlobs = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter(
            [-0.23481691199494992, 0.8993626256259108, -0.17161491976453003,
             0.8993626256259108, -0.23481691199494992, -0.17161491976453003,
             0.38167210983861377, -0.17161491976453003, -0.23481691199494992, 0.8993626256259108, -0.17161491976453003,
             0.8993626256259108, -0.23481691199494992],
            offset=convolution_helper.OFFSETS_DIAMOND_OOPS),
        activation=shaders.worm_activation()

    ),
    colour=GREEN
)

Smokey = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter(
            [-0.8645334276853669, -0.11383890930642826, 0.9837237749418761,
             -0.11383890930642826, -0.8645334276853669, 0.9837237749418761,
             0.9525922677120573, 0.9837237749418761, -0.8645334276853669, -0.11383890930642826, 0.9837237749418761,
             -0.11383890930642826, -0.8645334276853669],
            offset=convolution_helper.OFFSETS_DIAMOND_OOPS),
        activation=shaders.worm_activation()

    )
)

FragileWorms = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter(
            [0.8594494578896017, -0.9640521017172925, -0.375004031529216, -0.9640521017172925, 0.8594494578896017,
             -0.375004031529216, 0.7202524632699319, -0.375004031529216, 0.8594494578896017, -0.9640521017172925,
             -0.375004031529216, -0.9640521017172925, 0.8594494578896017],
            ),
        activation=shaders.worm_activation(),

    ),
    colour=RED
)

StableStars = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([
            0.21268162481624686, 0.3916401990256584, -0.9870163945448558,
            0.3916401990256584, 0.21268162481624686, -0.9870163945448558,
            0.46833060598727116, -0.9870163945448558, 0.21268162481624686, 0.3916401990256584, -0.9870163945448558,
            0.3916401990256584, 0.21268162481624686],
        ),
        activation=shaders.worm_activation(),

    ),
    colour=BLUE
)

DeathMetalWorms = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([
            -0.8641687418840689, 0.8393475265626524, 0.4971024953590484,
            0.8393475265626524, -0.8641687418840689, 0.4971024953590484,
            -0.3754929129934068, 0.4971024953590484, -0.8641687418840689, 0.8393475265626524, 0.4971024953590484,
            0.8393475265626524, -0.8641687418840689], convolution_helper.OFFSETS_DIAMOND_5
        ),
        activation=shaders.worm_activation(),

    ),
    colour=RED
)

BalooningWorm = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([

            0.6841829381556945, 0.09091730170215473, -0.9864762892163701,
            0.09091730170215473, 0.6841829381556945, -0.9864762892163701,
            -0.2047354187659145, -0.9864762892163701, 0.6841829381556945, 0.09091730170215473, -0.9864762892163701,
            0.09091730170215473, 0.6841829381556945
        ],
        ),
        activation=shaders.worm_activation(),

    ),
    colour=PINK
)

Lattice = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([
            0.7744369459749529, 0.2781675312739802, 0.7744369459749529,
            -0.9434019420809658, -0.9434019420809658, 0.2781675312739802,
            0.2781675312739802, -0.9434019420809658, -0.9434019420809658, 0.7744369459749529, 0.2781675312739802,
            0.7744369459749529
        ],
        ),
        activation=shaders.worm_activation(),

    ),
    colour=PINK
)

VolatileTopology = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([
            0.7524015049944961, -0.8505693461518442, 0.7524015049944961,
            0.468061137882269, 0.468061137882269, -0.8505693461518442,
            -0.5265149448846187, -0.8505693461518442, 0.468061137882269, 0.468061137882269, 0.7524015049944961,
            -0.8505693461518442, 0.7524015049944961

        ],
        ),
        activation=shaders.slime_activation(),

    ),
    colour=RED
)

BurningGliders = Preset(
    program=shaders.custom_shader(
        convolution_filter=convolution_helper.build_filter([
            0.6052346824736283, -0.7007063168957162, 0.6052346824736283,
            -0.35464393456875953, -0.35464393456875953, -0.7007063168957162,
            0.9704433352823121, -0.7007063168957162, -0.35464393456875953, -0.35464393456875953,
            0.6052346824736283, -0.7007063168957162, 0.6052346824736283

        ],
            offset=convolution_helper.OFFSETS_DIAMOND_5
        ),
        activation=shaders.slime_activation(),

    ),
    colour=RED
)
