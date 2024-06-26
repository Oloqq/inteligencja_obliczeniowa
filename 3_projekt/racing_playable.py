import gymnasium as gym
from gymnasium.utils.play import play
import numpy as np

mapping = {"w": np.array([0, 0.7, 0]),
           "a": np.array([-1, 0, 0]),
           "s": np.array([0, 0, 1]),
           "d": np.array([1, 0, 0]),
           "wa": np.array([-1, 0.7, 0]),
           "dw": np.array([1, 0.7, 0]),
           "ds": np.array([1, 0, 1]),
           "as": np.array([-1, 0, 1]),
           }
default_action = np.array([0, 0, 0])
env = gym.make("CarRacing-v2", render_mode="rgb_array")
# env.reset(options={'randomize': True})

# env.reset()
# for _ in range(10000):
#     env.step(np.array([0, 0.7, 0]))

seed = 1
env.reset(seed=seed)
for _ in range(100):
    action = np.array([0, 0.7, 0])
    env.step(action)

play(env, keys_to_action=mapping, noop=default_action)
# play(env, keys_to_action=mapping, noop=default_action)


# env = gym.make("CarRacing-v2", render_mode="human")
# play(env)
# observation, info = env.reset(seed=42)
# for _ in range(1000):
#     action = env.action_space.sample()  # this is where you would insert your policy
#     observation, reward, terminated, truncated, info = env.step(action)

#     if terminated or truncated:
#         observation, info = env.reset()

# env.close()
