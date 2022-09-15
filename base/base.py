from util import load_shader


def vertex() -> str:
    return load_shader("./base/vertex.glsl")

def frag() -> str:
    return load_shader("./base/frag.glsl")