from dataclasses import dataclass
from typing import Callable, TypeVar, Tuple
from typing import List
import random
def load_shader(path: str):
    with open(f"./shaders/{path}", "r") as f:
        return f.read()


Shader = Callable[[], str]
FragShader = Callable[[str], str]
ShaderCode = TypeVar(name="ShaderCode", bound=str)

Vec2 = TypeVar("Vec2", bound=Tuple[float])



OFFSETS_3x3 = [
    (-1, -1), (0, -1), (1, -1),
    (-1, 0),  (0, 0),  (1, 0),
    (-1, 1),  (0, 1),  ( 1, 1)
]

OFFSETS_DIAMOND = [
    (0,-2),
    (-1, -1), (0, -1), (1, -1),
    (-2, 0), (-1, 0), (0, 0), (1, 0), (2, 0),
    (-1, 1), (0, 1), (1, 1),
    (2, 0)
]


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

def symmetric_filter_3x3(corner: float, top: float, mid: float):
    return [
        corner,top,corner,
        top,mid,top,
        corner,top,corner
    ]

def symmetric_filter_diamond(point, edge, inner, mid):
    return [
        point,
        edge,inner,edge,
        point,inner,mid,inner,point,
        edge,inner,edge,
        point
    ]


def glsl_int_tuple(v: Vec2):
    return f"ivec2({v[0]},{v[1]})"

def convolve_filter_offset_glsl(filter: List[Tuple[float]]):
    return f"""
            ivec2 offsets[{len(filter)}] = ivec2[{len(filter)}](
                    {",".join([glsl_int_tuple(i) for i in filter])}
                );
        """

def random_float(abs_max: float):
    return ((random.random() - 0.5) * 2) * abs_max

def random_symetric(abs_max: float):
    c = random_float(abs_max)
    t = random_float(abs_max)
    m = random_float(abs_max)
    return symmetric_filter(c, t, m)

def random_filter():
    return [random_float(1) for i in range(9)]


def slime_activation():
    return "-1./(0.89*pow(x, 2.)+1.)+1."

def worm_activation():
    return "-1./pow(2., (0.6*pow(x, 2.)))+1."

# def custom_shader(convolve_vals: List[float], activation: str) -> ShaderCode:
#     def convolve_filter(convolve_filter: List[float]):
#         return ",".join([str(float(i)) for i in convolve_filter])
#
#     def custom_activation(expr: str):
#         return f"float activate(float x){{ return {expr};}}"

@dataclass
class Convolution_Filter:
    """
    The offsets of the cells we want to use in the convolution and the values used for mulitplying them
    Must be the same length and in the same order
    """
    convolution_values: List[float]
    convolution_offsets: List[Vec2]



def custom_activation(expr: str):
    return f"float activate(float x){{ return {expr};}}"

def slime_activation():
    return "-1./(0.89*pow(x, 2.)+1.)+1."

def custom_shader(convolution_filter: Convolution_Filter, activation: str) -> ShaderCode:
    def comma_sep_floats(convolve_filter: List[float]):
        return ",".join([str(float(i)) for i in convolve_filter])
    n_filters = len(convolution_filter.convolution_values)
    glsl = f"""
        #version 330
        uniform sampler2D Texture;
        out float out_vert;
        out float last_vert;
        float cell(int x, int y) {{
            ivec2 tSize = textureSize(Texture, 0).xy;
            return texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0).r;
        }}        
        {custom_activation(activation)}
        void main() {{
            int width = textureSize(Texture, 0).x;
            ivec2 in_text = ivec2(gl_VertexID % width, gl_VertexID / width);
            float convolve_filter[{n_filters}] = float[{n_filters}](
                       {comma_sep_floats(convolution_filter.convolution_values)}
            );
            {convolve_filter_offset_glsl(convolution_filter.convolution_offsets)}

            float convolve_sum = 0;
            for (int i=0;i<{len(convolution_filter.convolution_values)};i++){{
                convolve_sum += cell(in_text.x + offsets[i].x, in_text.y + offsets[i].y) * convolve_filter[i];
            }}
            out_vert = activate(convolve_sum);
        }}
    """
    print(glsl)
    return glsl