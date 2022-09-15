from abc import ABC, abstractmethod
from typing import Callable, TypeVar
import os

def load_shader(path: str):
    with open(f"./shaders/{path}", "r") as f:
        return f.read()


Shader = Callable[[], str]
FragShader = Callable[[str], str]
ShaderCode = TypeVar(name="ShaderCode", bound=str)


def Vertex() -> ShaderCode:
    return """  
        #version 330
        
        in vec2 in_vert;
        in vec2 in_texcoord;
        
        out vec2 v_text;
        
        void main() {
            v_text = in_texcoord;
            gl_Position = vec4(in_vert, 0.0, 1.0);
        }
    """

def insert(n: float, invert: bool):
    if invert:
        return 1 -n
    else:
        return n

def Frag(r: float, g: float, b: float, invert=False) -> ShaderCode:
    return f"""
    #version 330
    uniform sampler2D Texture;
    in vec2 v_text;
    out vec4 f_color;
    void main() {{
        float factor = texture(Texture, v_text).r;
        f_color = vec4({insert(r, invert)}*factor,{insert(b,invert)}*factor,{insert(g,invert)}*factor,1.);
    }}
"""

def Worm() -> ShaderCode:
    return load_shader("worms.glsl")

def Slime() -> ShaderCode:
    return load_shader("slime.glsl")

def Conway() -> ShaderCode:
    return load_shader("conway.glsl")

