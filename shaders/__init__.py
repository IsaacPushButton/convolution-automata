from dataclasses import dataclass
from typing import Callable, TypeVar, Tuple
from typing import List
import random
import convolution_helper
from const import Vec2


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
        return 1 - n
    else:
        return n


def Frag() -> ShaderCode:
    return f"""
    #version 330
    uniform sampler2D Texture;
    in vec2 v_text;
    out vec4 f_color;
    void main() {{
        f_color = texture(Texture, v_text);
    }}
"""


def Worm() -> ShaderCode:
    return load_shader("worms.glsl")


def Slime() -> ShaderCode:
    return load_shader("slime.glsl")


def Conway() -> ShaderCode:
    return load_shader("conway.glsl")


def comma_sep_floats(floats: List[float]):
    return ",".join([str(float(i)) for i in floats])


def glsl_int_tuple(v: Vec2):
    return f"ivec2({v[0]},{v[1]})"


def convolve_filter_offset_glsl(filter: List[Vec2], var_suffix: str):
    return f"""
            ivec2 offsets_{var_suffix}[{len(filter)}] = ivec2[{len(filter)}](
                    {",".join([glsl_int_tuple(i) for i in filter])}
                );
        """


def convolve_filter_values_glsl(filter: List[float], _len: int, var_suffix: str):
    return f"""
        float convolve_filter_{var_suffix}[{_len}] = float[{_len}](
                           {comma_sep_floats(filter)}
                           
                );
    """


def slime_activation():
    return "-1./(0.89*pow(x, 2.)+1.)+1."


def worm_activation():
    return "-1./pow(2., (0.6*pow(x, 2.)))+1."


def custom_activation(expr: str):
    return f"float activate(float x){{ return {expr};}}"


def custom_shader(convolution_filters: List[convolution_helper.ConvolutionFilter], activation: str,
                  red_relation: List[float] = None, blue_relation: List[float] = None, green_relation: List[float] = None) -> ShaderCode:
    convolve_glsl_block = ""

    cols = ["red", "green", "blue"]
    col_dict = {
        "red" :  red_relation if red_relation else [0,0,0],
        "blue" : blue_relation if blue_relation else [0,0,0],
        "green" : green_relation if green_relation else [0,0,0]
    }
    for col, fil in zip(cols, convolution_filters):
        convolve_glsl_block += f"""
            float {col} = 0.;
            {convolve_filter_values_glsl(fil.convolution_values, len(fil.convolution_offsets), col)}
            {convolve_filter_offset_glsl(fil.convolution_offsets, col)}
            for (int i=0;i<{len(fil.convolution_values)};i++){{
                {col} -= cell_{col}(in_text.x + offsets_{col}[i].x, in_text.y + offsets_{col}[i].y) * convolve_filter_{col}[i];
            }}
            
            
            //{col} = activate({col});
        """
    for col in cols:
        convolve_glsl_block += f"""
            
            {col} += {cols[0]} * {col_dict[col][0]};
            {col} -= {cols[1]} * {col_dict[col][1]};
            {col} -= {cols[2]} * {col_dict[col][2]};

            {col} = activate({col});
               """

    glsl = f"""
        #version 330
        uniform sampler2D Texture;
        out vec3 out_vert;
        ivec2 tSize = textureSize(Texture, 0).xy;
        
        {custom_activation(activation)}

        float cell_red(int x, int y) {{
            vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
            return tex.r;
        }}     
        float cell_green(int x, int y) {{
            vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
            return tex.g;
        }}   
        float cell_blue(int x, int y) {{
            vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
            return tex.b;
        }}   
    
        void main() {{
            int width = textureSize(Texture, 0).x;
            ivec2 in_text = ivec2(gl_VertexID % tSize[0], gl_VertexID / tSize[0]);
            {convolve_glsl_block}
            
            out_vert = vec3({",".join(cols)});
        }}
    """
    print(glsl)
    return glsl
