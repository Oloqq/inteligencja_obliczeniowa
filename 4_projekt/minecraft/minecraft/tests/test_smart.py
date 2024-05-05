import gymnasium
import numpy as np
import time

import minecraft


def play(audio_on=True, render_mode="human"):
    env = gymnasium.make(
        "Minecraft-v0", audio_on=audio_on, render_mode=render_mode
    )
    obs, _ = env.reset()
    while True:
        action = 0
        steve, creeper = obs
        if steve == creeper:
            if steve == 0:
                action = 2
            elif steve == 1:
                action = np.random.randint(1, 3)
            else:
                action = 1

        time.sleep(0.3)

        # Processing:
        obs, _, done, _, info = env.step(action)

        # print(f"Obs: {obs}\n" f"Score: {info['score']}\n")

        if done:
            break

    env.close()
    assert obs.shape == env.observation_space.shape
    assert info["score"] == 0

if __name__ == "__main__":
    play()
