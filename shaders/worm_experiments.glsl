#version 330

uniform sampler2D Texture;
uniform float noise;
uniform float frequency;
out float out_vert;

#define FILTER_SIZE 3

ivec2 tSize;

float cell(int x, int y) {
    return texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0).r;
}

float worm(float x) {
    return -1./pow(2., (0.6*pow(x, 2.)))+1.;
}

float inverse_gaussian(float x) {
    return -1.0 / pow(2.0, (0.6 * pow(x, 2.0))) + 1.0;
}

float sigmoid(float x) {
    return 1.0 / (1.0 + exp(-x));
}

float tanh_activation(float x) {
    return tanh(x);
}

float relu(float x) {
    return max(0.0, x);
}


float leaky_relu(float x) {
    return max(0.01 * x, x);
}

float prelu(float x, float alpha) {
    return max(alpha * x, x);
}

float elu(float x, float alpha) {
    return x > 0.0 ? x : alpha * (exp(x) - 1.0);
}

float selu(float x, float alpha, float lambda) {
    return x > 0.0 ? lambda * x : lambda * (alpha * exp(x) - alpha);
}

float swish(float x, float beta) {
    return x * (1.0 / (1.0 + exp(-beta * x)));
}

float gaussian(float x) {
    float sigma = 1.0;
    return exp(-x * x / (2.0 * sigma * sigma));
}

float softplus(float x) {
    return log(1.0 + exp(x));
}
float softsign(float x) {
    return x / (1.0 + abs(x));
}

float bent_identity(float x) {
    return (sqrt(x * x + 1.0) - 1.0) / 2.0 + x;
}

float isru(float x, float alpha) {
    return x / sqrt(1.0 + alpha * x * x);
}

float inverse_quadratic(float x){
    return -1./(0.89*pow(x, 2.)+1.)+1.;
}

float combined_activation(float x, float weight) {
    float inv_gauss = inverse_gaussian(x);
    float r = inverse_quadratic(x);
    return weight * inv_gauss + (1.0 - weight) * r;
}

void main() {
    tSize = textureSize(Texture, 0).xy;
    ivec2 in_text = ivec2(gl_VertexID % tSize.x, gl_VertexID / tSize.y);
    float convolve_filter[9] = float[9](
                0.66,-0.9,0.66,
                -0.9,-0.66,-0.9,
                0.66,-0.9,0.66
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
    float asd=  noise;
    //out_vert = combined_activation(convolve_sum, 1- (noise*0.00000000001));
    out_vert = worm(convolve_sum);
}
