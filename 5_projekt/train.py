import gymnasium as gym
from stable_baselines3 import SAC
from stable_baselines3.common.env_util import make_vec_env

env = gym.make("LunarLander-v2",
    continuous = True,
    gravity = -10.0,
    enable_wind = False,
    wind_power = 15.0,
    turbulence_power = 1.5,
    # render_mode="human"
)

model = SAC('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=10000)
model.save("sac_lunarlander_continuous")

# obs = env.reset()
# for i in range(1000):
#     print(i)
#     action, _states = model.predict(obs, deterministic=True)
#     obs, reward, done, info = env.step(action)
#     env.render()
#     if done:
#         obs = env.reset()

env.close()