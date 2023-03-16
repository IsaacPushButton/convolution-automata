import presets
import shaders
from window import new_window, GameConfig, Skip

if __name__ == '__main__':
    window = new_window(GameConfig(
        window_size=(1000, 1000),
        texture_size=(600, 600),
        desired_fps=30,
        skip=Skip.NoSkip,
        preset=presets.MulipleNeighbours,
        pause_start=False
    ))
    window.run()
