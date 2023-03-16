
#version 330

uniform sampler2D Texture;

out float out_vert;
out vec3 last_vert;
float cell(int x, int y) {
    ivec2 tSize = textureSize(Texture, 0).xy;
    return texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0).r;
}


float inverse_gaussian(float x) {
  return -1./pow(2., (0.6*pow(x, 2.)))+1.;
}

float activate(float x) {
  return inverse_gaussian(x);
}


void main() {
    int width = textureSize(Texture, 0).x;
    ivec2 in_text = ivec2(gl_VertexID % width, gl_VertexID / width);
    float convolve_filter[9] = float[9](
                0.68,-0.9,0.68,
                -0.9,-0.66,-0.9,
                0.68,-0.9,0.68
    );

    ivec2 offsets[9] = ivec2[9](
        ivec2(-1,-1),
        ivec2(0,-1),
        ivec2(1,-1),
        ivec2(-1,0),
        ivec2(0,0),
        ivec2(1,0),
        ivec2(-1,1),
        ivec2(0,1),
        ivec2(1,1)
    );

    float convolve_sum = 0;
    for (int i=0;i<9;i++){
        convolve_sum += cell(in_text.x + offsets[i].x, in_text.y + offsets[i].y) * convolve_filter[i];
    }
    out_vert = (activate(convolve_sum), 1.0, 1.0);
}
