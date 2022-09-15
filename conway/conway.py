from util import load_shader


def conway_shader() -> str:
    return load_shader("./conway/worms.glsl")