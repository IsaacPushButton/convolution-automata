import presets
from window import new_window, GameConfig, Skip

if __name__ == '__main__':
    window = new_window(GameConfig(
        window_size=(800, 800),
        texture_size=(800, 800),
        desired_fps=60,
        skip=Skip.Even,
        preset=presets.Worms,
        pause_start=False
    ))
    window.run()
