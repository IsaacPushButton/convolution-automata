
def load_shader(path: str):
    with open(path, "r") as f:
        return f.read()

vertex = load_shader("shaders/base/vertex.glsl")
frag = load_shader("shaders/base/frag.glsl")
worm = load_shader("shaders/worms.glsl")
slime = load_shader("shaders/slime.glsl")
conway = load_shader("shaders/conway.glsl")

