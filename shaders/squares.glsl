#version 330
uniform sampler2D Texture;
out vec3 out_vert;
ivec2 tSize = textureSize(Texture, 0).xy;

float activate(float x){ return -1./pow(2., (0.6*pow(x, 2.)))+1.;}

float cell_red(int x, int y) {
    vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
    return tex.r + (1 - activate((tex.g) + (tex.b)));
}
float cell_green(int x, int y) {
    vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
    return tex.g + activate((1 - (tex.b) + (tex.r))) ;
}
float cell_blue(int x, int y) {
    vec4 tex = texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0);
    return tex.b + activate((1 - (tex.r) + (tex.g )));
}

void main() {
    int width = textureSize(Texture, 0).x;
    ivec2 in_text = ivec2(gl_VertexID % tSize[0], gl_VertexID / tSize[0]);

    float red = 0.;

float convolve_filter_red[12] = float[12](
                   -0.7698947641508884,0.4221577331409698,-0.7698947641508884,0.3712341212048773,0.3712341212048773,0.4221577331409698,0.4221577331409698,0.3712341212048773,0.3712341212048773,-0.7698947641508884,0.4221577331409698,-0.7698947641508884

        );


    ivec2 offsets_red[12] = ivec2[12](
            ivec2(-1,-2),ivec2(0,-2),ivec2(1,-2),ivec2(-2,-1),ivec2(2,-1),ivec2(-2,0),ivec2(2,0),ivec2(-2,1),ivec2(2,1),ivec2(-1,2),ivec2(0,2),ivec2(1,2)
        );

    for (int i=0;i<12;i++){
        red += cell_red(in_text.x + offsets_red[i].x, in_text.y + offsets_red[i].y) * convolve_filter_red[i];
    }
    red = activate(red);

    float green = 0.;

float convolve_filter_green[9] = float[9](
                   -0.3025457843429351,0.20738677180744092,-0.3025457843429351,0.20738677180744092,-0.8113491839221418,0.20738677180744092,-0.3025457843429351,0.20738677180744092,-0.3025457843429351

        );


    ivec2 offsets_green[9] = ivec2[9](
            ivec2(-1,-1),ivec2(0,-1),ivec2(1,-1),ivec2(-1,0),ivec2(0,0),ivec2(1,0),ivec2(-1,1),ivec2(0,1),ivec2(1,1)
        );

    for (int i=0;i<9;i++){
        green += cell_green(in_text.x + offsets_green[i].x, in_text.y + offsets_green[i].y) * convolve_filter_green[i];
    }
    green = activate(green);

    float blue = 0.;

float convolve_filter_blue[13] = float[13](
                   0.6013679064822279,0.4055633010708466,-0.6768359444825607,0.4055633010708466,0.6013679064822279,-0.6768359444825607,0.5629809785146389,-0.6768359444825607,0.6013679064822279,0.4055633010708466,-0.6768359444825607,0.4055633010708466,0.6013679064822279

        );


    ivec2 offsets_blue[13] = ivec2[13](
            ivec2(0,-2),ivec2(-1,-1),ivec2(0,-1),ivec2(1,-1),ivec2(-2,0),ivec2(-1,0),ivec2(0,0),ivec2(1,0),ivec2(2,0),ivec2(-1,1),ivec2(0,1),ivec2(1,1),ivec2(0,2)
        );

    for (int i=0;i<13;i++){
        blue += cell_blue(in_text.x + offsets_blue[i].x, in_text.y + offsets_blue[i].y) * convolve_filter_blue[i];
    }
    blue = activate(blue);


    out_vert = vec3(red,green,blue);
}
