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

    def set_color(self, r: float, g: float, b: float, invert=False) -> 'Preset':
        self.frag = shaders.Frag(r, g, b, invert)
        return self


class Conway(Preset):
    program = shaders.Conway()

class Slime(Preset):
    program = shaders.Slime()

class Worms(Preset):
    program = shaders.Worm()