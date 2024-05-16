import gymnasium as gym

env = gym.make("LunarLander-v2",
    continuous = False,
    gravity = -10.0,
    enable_wind = False,
    wind_power = 15.0,
    turbulence_power = 1.5,
)

env.reset()
for _ in range(1000):
    env.step(env.action_space.sample())
    env.render()