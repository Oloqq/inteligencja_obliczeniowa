import gymnasium as gym

env = gym.make("LunarLander-v2",
    continuous = False,
    gravity = -10.0,
    enable_wind = False,
    wind_power = 15.0,
    turbulence_power = 1.5,
    render_mode="human"
)

env.reset()
for i in range(1000):
    # print(i)
    next_state, reward, done, _, _  = env.step(env.action_space.sample())
    print(reward)
    env.render()