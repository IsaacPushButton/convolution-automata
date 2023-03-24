import presets
import shaders
from window import new_window, GameConfig, Skip

if __name__ == '__main__':
    window = new_window(GameConfig(
        window_size=(1000, 1000),
        texture_size=(1000, 1000),
        desired_fps=60,
        skip=Skip.Odd,
        preset=presets.Worms,
        pause_start=False
    ))
    window.run()
