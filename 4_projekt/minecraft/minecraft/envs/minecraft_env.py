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
)

class Actions(IntEnum):
    IDLE, FLAP = 0, 1

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

        # self._get_observation = self._get_observation_features # TODO restore

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
        reward = None

        self._sound_cache = None
        if action == Actions.FLAP:
            self._player_x += 1

        # check for score
        # player_mid_pos = self._player_x + PLAYER_WIDTH / 2
        # for pipe in self._upper_pipes:
        #     pipe_mid_pos = pipe["x"] + PIPE_WIDTH / 2
        #     if pipe_mid_pos <= player_mid_pos < pipe_mid_pos + 4:
        #         self._score += 1
        #         reward = 1  # reward for passed pipe
        #         self._sound_cache = "point"

        # player's movement
        # if self._player_vel_y < PLAYER_MAX_VEL_Y and not self._player_flapped:
        #     self._player_vel_y += PLAYER_ACC_Y

        # if self._player_flapped:
        #     self._player_flapped = False

        #     # more rotation to cover the threshold
        #     # (calculated in visible rotation)
        #     self._player_rot = 45

        # move pipes to left
        # for up_pipe, low_pipe in zip(self._upper_pipes, self._lower_pipes):
        #     up_pipe["x"] += PIPE_VEL_X
        #     low_pipe["x"] += PIPE_VEL_X

        #     # it is out of the screen
        #     if up_pipe["x"] < -PIPE_WIDTH:
        #         new_up_pipe, new_low_pipe = self._get_random_creeper()
        #         up_pipe["x"] = new_up_pipe["x"]
        #         up_pipe["y"] = new_up_pipe["y"]
        #         low_pipe["x"] = new_low_pipe["x"]
        #         low_pipe["y"] = new_low_pipe["y"]

        if self.render_mode == "human":
            self.render()

        obs = ()
        # obs, reward_private_zone = self._get_observation()
        # if reward is None:
        #     if reward_private_zone is not None:
        #         reward = reward_private_zone
        #     else:
        #         reward = 0.1  # reward for staying alive

        # agent touch the top of the screen as punishment
        if self._player_y < 0:
            reward = -0.5

        # check for crash
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
        self._creepers = [awww_maaaan]

        if self.render_mode == "human":
            self.render()

        # obs, _ = self._get_observation() # TODO restore
        obs = ()
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
        # if player crashes into ground
        # if self._player_y + PLAYER_HEIGHT >= self._ground["y"] - 1:
        #     return True
        # else:
        #     player_rect = pygame.Rect(
        #         self._player_x, self._player_y, PLAYER_WIDTH, PLAYER_HEIGHT
        #     )

            # for up_pipe, low_pipe in zip(self._upper_pipes, self._lower_pipes):
            #     # upper and lower pipe rects
            #     up_pipe_rect = pygame.Rect(
            #         up_pipe["x"], up_pipe["y"], PIPE_WIDTH, PIPE_HEIGHT
            #     )
            #     low_pipe_rect = pygame.Rect(
            #         low_pipe["x"], low_pipe["y"], PIPE_WIDTH, PIPE_HEIGHT
            #     )

            #     # check collision
            #     up_collide = player_rect.colliderect(up_pipe_rect)
            #     low_collide = player_rect.colliderect(low_pipe_rect)

            #     if up_collide or low_collide:
            #         return True

        return False

    def _get_observation_features(self) -> np.ndarray:
        pipes = []
        for up_pipe, low_pipe in zip(self._upper_pipes, self._lower_pipes):
            # the pipe is behind the screen?
            if low_pipe["x"] > self._screen_width:
                pipes.append((self._screen_width, 0, self._screen_height))
            else:
                pipes.append(
                    (low_pipe["x"], (up_pipe["y"] + PIPE_HEIGHT), low_pipe["y"])
                )

        pipes = sorted(pipes, key=lambda x: x[0])
        pos_y = self._player_y
        vel_y = self._player_vel_y
        rot = self._player_rot

        if self._normalize_obs:
            pipes = [
                (
                    h / self._screen_width,
                    v1 / self._screen_height,
                    v2 / self._screen_height,
                )
                for h, v1, v2 in pipes
            ]
            pos_y /= self._screen_height
            vel_y /= PLAYER_MAX_VEL_Y
            rot /= 90

        return (
            np.array(
                [
                    pipes[0][0],  # the last pipe's horizontal position
                    pipes[0][1],  # the last top pipe's vertical position
                    pipes[0][2],  # the last bottom pipe's vertical position
                    pipes[1][0],  # the next pipe's horizontal position
                    pipes[1][1],  # the next top pipe's vertical position
                    pipes[1][2],  # the next bottom pipe's vertical position
                    pipes[2][0],  # the next next pipe's horizontal position
                    pipes[2][1],  # the next next top pipe's vertical position
                    pipes[2][2],  # the next next bottom pipe's vertical position
                    pos_y,  # player's vertical position
                    vel_y,  # player's vertical velocity
                    rot,  # player's rotation
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
        """Re-draws the renderer's surface.

        This method updates the renderer's surface by re-drawing it according to
        the current state of the game.

        Args:
            show_score (bool): Whether to draw the player's score or not.
        """
        # Background
        self._surface.blit(self._images["background"], (0, 0))

        # Pipes
        # for up_pipe, low_pipe in zip(self._upper_pipes, self._lower_pipes):
        #     self._surface.blit(self._images["pipe"][0], (up_pipe["x"], up_pipe["y"]))
        #     self._surface.blit(self._images["pipe"][1], (low_pipe["x"], low_pipe["y"]))


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
