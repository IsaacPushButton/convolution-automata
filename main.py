import presets
import shaders
from window import new_window, GameConfig, Skip

if __name__ == '__main__':
    window = new_window(GameConfig(
        window_size=(1200,1200),
        texture_size=(1000, 1000),
        desired_fps=60,
        skip=Skip.Even,
        preset=presets.Preset(
            program=shaders.custom_shader(
                convolution_filter=shaders.Convolution_Filter(
                    shaders.symmetric_filter_diamond(-0.5,0.9, 0.2, -0.8),
                    shaders.OFFSETS_DIAMOND
                ),
                activation=shaders.slime_activation()
            )
        ),
))
    window.run()


