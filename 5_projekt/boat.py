import gymnasium as gym
from stable_baselines3 import SAC

env = gym.make("LunarLander-v2",
    continuous = True,
    gravity = -10.0,
    enable_wind = False,
    wind_power = 15.0,
    turbulence_power = 1.5,
    render_mode="human"
)

# Załadowanie wcześniej zapisanego modelu
model = SAC.load("sac_lunarlander_continuous", env=env)

# Testowanie załadowanego modelu
obs, info = env.reset()
for i in range(1000):
    print(i)
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info, idk = env.step(action)
    env.render()
    if done:
        obs = env.reset()

env.close()
