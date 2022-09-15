def load_shader(path: str):
    with open(path, "r") as f:
        return f.read()