from enum import IntEnum
from itertools import cycle
from typing import Dict, Optional, Tuple, Union

import gymnasium
import numpy as np
import pygame

from minecraft.envs import utils
from minecraft.envs.constants import (
    WINDOW_WIDTH, WINDOW_HEIGHT,
    PLAYER_WIDTH, PLAYER_HEIGHT,
    CREEPER_WIDTH, CREEPER_HEIGHT,
)

class Actions(IntEnum):
    IDLE, LEFT, RIGHT = 0, 1, 2

class MinecraftEnv(gymnasium.Env):
    # Required by parent class
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}

    def __init__(
        self,
        screen_size: Tuple[int, int] = (WINDOW_WIDTH, WINDOW_HEIGHT),
        audio_on: bool = False,
        normalize_obs: bool = True,
        render_mode: Optional[str] = None,
        background: Optional[str] = "day",
        score_limit: Optional[int] = None,
        debug: bool = False
    ) -> None:
        assert render_mode is None or render_mode == "human"
        self.render_mode = render_mode
        self._debug = debug
        self._score_limit = score_limit

        self.action_space = gymnasium.spaces.Discrete(2)
        if normalize_obs:
            self.observation_space = gymnasium.spaces.Box(
                -1.0, 1.0, shape=(12,), dtype=np.float64
            )
        else:
            self.observation_space = gymnasium.spaces.Box(
                -np.inf, np.inf, shape=(12,), dtype=np.float64
            )

        self._screen_width = screen_size[0]
        self._screen_height = screen_size[1]
        self._normalize_obs = normalize_obs
        self._audio_on = audio_on
        self._sound_cache = None
        self._bg_type = background

        self._creepers = []

        self._get_observation = self._get_observation_features

        if render_mode is not None:
            self._fps_clock = pygame.time.Clock()
            self._display = None
            self._surface = pygame.Surface(screen_size)
            self._images = utils.load_images(convert=False)
            if audio_on:
                self._sounds = utils.load_sounds()

    def step(self, action: Union[Actions, int],
    ) -> Tuple[np.ndarray, float, bool, Dict]:
        terminal = False
        reward = 0

        self._sound_cache = None
        if action == Actions.RIGHT and self._player_x < 2:
            self._player_x += 1
        if action == Actions.LEFT and self._player_x > 0:
            self._player_x -= 1

        aww_meeeeen = []
        for col, row in self._creepers:
            new_row = row + 1
            if new_row >= 3:
                if col == self._player_x:
                    print("ooohh")
                    self._score = max(self._score - 5, 0)
                    reward -= 5
                else:
                    self._score += 1
                    reward += 1
                aww_meeeeen.append((self._get_random_creeper(), 0))
            else:
                aww_meeeeen.append((col, new_row))
        self._creepers = aww_meeeeen

        if self.render_mode == "human":
            self.render()

        obs, reward_private_zone = self._get_observation()
        if reward is None:
            if reward_private_zone is not None:
                reward = reward_private_zone
            else:
                reward = 0.1

        # FIXME check for crash
        if self._check_crash():
            self._sound_cache = "hit"
            reward = -1  # reward for dying
            terminal = True
            self._player_vel_y = 0
        info = {"score": self._score}

        return (
            obs,
            reward,
            terminal,
            (self._score_limit is not None) and (self._score >= self._score_limit),
            info,
        )

    # Options are declared just to supress a warning
    def reset(self, seed=None, options=None):
        """Resets the environment (starts a new game)."""
        super().reset(seed=seed)

        # Player's info:
        self._player_x = 1
        self._player_y = 10
        self._player_vel_y = -9  # player"s velocity along Y
        self._player_rot = 45  # player"s rotation
        self._player_idx = 0
        self._loop_iter = 0
        self._score = 0

        awww_maaaan = self._get_random_creeper()
        self._creepers = [(awww_maaaan, 0)]

        if self.render_mode == "human":
            self.render()

        obs, _ = self._get_observation()
        info = {"score": self._score}
        return obs, info

    def render(self) -> None:
        """Renders the next frame."""
        if self.render_mode == "rgb_array": # FIXME needed?
            self._draw_surface(show_score=False)
            # Flip the image to retrieve a correct aspect
            return np.transpose(pygame.surfarray.array3d(self._surface), axes=(1, 0, 2))
        else:
            self._draw_surface(show_score=True)
            if self._display is None:
                self._make_display()

            self._update_display()
            self._fps_clock.tick(self.metadata["render_fps"])

    def close(self):
        """Closes the environment."""
        if self.render_mode is not None:
            pygame.display.quit()
            pygame.quit()
        super().close()

    def _get_random_creeper(self) -> Dict[str, int]:
        return self.np_random.integers(0, 3)

    def _check_crash(self) -> bool:
        """Returns True if player collides with the ground (base) or a pipe."""
        # crep = self._creepers[0]
        # aww, men = crep
        # if self._player_x == aww and men >= 2:
        #     return True

        return False

    def _get_observation_features(self) -> np.ndarray:
        return (
            np.array(
                [
                    self._player_x,
                    self._creepers[0][0] # creeper x
                ]
            ),
            None,
        )

    def _make_display(self) -> None:
        """Initializes the pygame's display.

        Required for drawing images on the screen.
        """
        self._display = pygame.display.set_mode(
            (self._screen_width, self._screen_height)
        )
        for name, value in self._images.items():
            if value is None:
                continue

            if type(value) in (tuple, list):
                self._images[name] = tuple([img.convert_alpha() for img in value])
            else:
                self._images[name] = (
                    value.convert() if name == "background" else value.convert_alpha()
                )

    def _draw_score(self) -> None:
        """Draws the score in the center of the surface."""
        score_digits = [int(x) for x in list(str(self._score))]
        total_width = 0  # total width of all numbers to be printed

        for digit in score_digits:
            total_width += self._images["numbers"][digit].get_width()

        x_offset = (self._screen_width - total_width) / 2

        for digit in score_digits:
            self._surface.blit(
                self._images["numbers"][digit], (x_offset, self._screen_height * 0.1)
            )
            x_offset += self._images["numbers"][digit].get_width()

    def _draw_surface(self, show_score: bool = True) -> None:
        self._surface.blit(self._images["background"], (0, 0))

        #   column, row
        for awwwww, meeeeen in self._creepers:
            self._surface.blit(
                self._images["creeper"],
                (awwwww * CREEPER_WIDTH, meeeeen * CREEPER_HEIGHT)
                )

        # Score
        # (must be drawn before the player, so the player overlaps it)
        if show_score:
            self._draw_score()

        # Player
        player_surface = pygame.transform.rotate(self._images["player"][self._player_idx], 0)
        player_surface_rect = player_surface.get_rect(
            topleft=(self._player_x * PLAYER_WIDTH, WINDOW_HEIGHT - PLAYER_HEIGHT)
        )
        self._surface.blit(player_surface, player_surface_rect)

    def _update_display(self) -> None:
        """Updates the display with the current surface of the renderer.

        A call to this method is usually preceded by a call to
        :meth:`.draw_surface()`. This method simply updates the display by
        showing the current state of the renderer's surface on it, it doesn't
        make any change to the surface.
        """
        if self._display is None:
            raise RuntimeError(
                "Tried to update the display, but a display hasn't been "
                "created yet! To create a display for the renderer, you must "
                "call the `make_display()` method."
            )

        pygame.event.get()
        self._display.blit(self._surface, [0, 0])
        pygame.display.update()

        # Sounds:
        if self._audio_on and self._sound_cache is not None:
            self._sounds[self._sound_cache].play()
