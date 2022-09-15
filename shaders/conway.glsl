
#version 330

uniform sampler2D Texture;

out float out_vert;

#define LIVING 0.0
#define DEAD 1.0

bool cell(int x, int y) {
    // get the texture size
    ivec2 tSize = textureSize(Texture, 0).xy;
    // Ensure lookups are not going outside the texture area because
    // texelFetch do not support texture repeat / wrap modes
    return texelFetch(Texture, ivec2((x + tSize.x) % tSize.x, (y + tSize.y) % tSize.y), 0).r < 0.5;
}

void main() {
    int width = textureSize(Texture, 0).x;
    ivec2 in_text = ivec2(gl_VertexID % width, gl_VertexID / width);
    bool living = cell(in_text.x, in_text.y);

    int neighbours = 0;
    if (cell(in_text.x - 1, in_text.y - 1)) neighbours++;
    if (cell(in_text.x - 1, in_text.y + 0)) neighbours++;
    if (cell(in_text.x - 1, in_text.y + 1)) neighbours++;
    if (cell(in_text.x + 1, in_text.y - 1)) neighbours++;
    if (cell(in_text.x + 1, in_text.y + 0)) neighbours++;
    if (cell(in_text.x + 1, in_text.y + 1)) neighbours++;
    if (cell(in_text.x + 0, in_text.y + 1)) neighbours++;
    if (cell(in_text.x + 0, in_text.y - 1)) neighbours++;

    if (living) {
        out_vert = (neighbours == 2 || neighbours == 3) ? LIVING : DEAD;
    } else {
        out_vert = (neighbours == 3) ? LIVING : DEAD;
    }
}
