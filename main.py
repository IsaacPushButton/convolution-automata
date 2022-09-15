import presets
import shaders
from shaders import custom_shader, symmetric_filter
from window import new_window, GameConfig, Skip

if __name__ == '__main__':
    window = new_window(GameConfig(
        window_size=(1200,1200),
        texture_size=(1000, 1000),
        desired_fps=60,
        skip=Skip.Even,
        preset=presets.Preset(program=shaders.Worm()),
))
    window.run()


