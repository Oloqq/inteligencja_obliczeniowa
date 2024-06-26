import gymnasium
import numpy as np
import time

import minecraft


def play(audio_on=True, render_mode="human"):
    env = gymnasium.make(
        "Minecraft-v0", audio_on=audio_on, render_mode=render_mode
    )
    obs = env.reset()
    while True:
        # Getting random action:
        action = np.random.randint(0, 3)

        time.sleep(0.3)

        # Processing:
        obs, _, done, _, info = env.step(action)

        print(f"Obs: {obs}\n" f"Score: {info['score']}\n")

        if done:
            break

    env.close()
    assert obs.shape == env.observation_space.shape
    assert info["score"] == 0

if __name__ == "__main__":
    play()
