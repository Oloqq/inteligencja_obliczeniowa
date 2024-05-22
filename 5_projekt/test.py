import gymnasium as gym
from stable_baselines3 import SAC
import numpy as np
import matplotlib.pyplot as plt
from stable_baselines3.common.vec_env import DummyVecEnv, VecMonitor


# Funkcja do trenowania modelu i zwracania nagród
def train_and_evaluate(env_name, hyperparams, num_timesteps=50000, num_runs=10):
    all_rewards = []

    for run in range(num_runs):
        env = gym.make(env_name, render_mode="rgb_array")
        # env = gym.make(
        #     "LunarLander-v2",
        #     continuous=True,
        #     gravity=-10.0,
        #     enable_wind=False,
        #     wind_power=15.0,
        #     turbulence_power=1.5,
        #     # render_mode="human"
        # )
        env = DummyVecEnv([lambda: env])
        env = VecMonitor(env)
        model = SAC("MlpPolicy", env, **hyperparams, verbose=0)
        model.learn(total_timesteps=num_timesteps)

        obs = env.reset()
        rewards = []
        for _ in range(num_timesteps):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            # print(rewards)
            rewards.append(np.mean(reward))
            # Upewnij się, że dodajesz jednowymiarowe wartości
            if done.any():
                obs = env.reset()

        all_rewards.append(rewards)
        env.close()

    all_rewards = np.array(all_rewards).clip(min=-10, max=10)
    mean_rewards = np.mean(all_rewards, axis=0)
    std_rewards = np.std(all_rewards, axis=0)

    return mean_rewards, std_rewards, all_rewards


# Definiowanie hiperparametrów
hyperparams_list = [
    # {"learning_rate": 0.0001, "gamma": 0.95},
    {
        "learning_rate": 0.0001,
        "gamma": 0.95,
        "batch_size": 64,
        # "update_frequency": 4,
        "tau": 0.01,
        # "alpha": 0.2,
    },
]

env_name = "Pendulum-v1"
num_timesteps = 300

# Trenowanie i zbieranie nagród dla różnych zestawów hiperparametrów
for i, hyperparams in enumerate(hyperparams_list):
    mean_rewards, std_rewards, all_rewards = train_and_evaluate(
        env_name, hyperparams, num_timesteps
    )
    # Rysowanie wykresu
    timesteps = np.arange(num_timesteps)
    plt.figure(figsize=(14, 7))
    plt.title(str(hyperparams))
    for reward in all_rewards:
        plt.plot(timesteps, reward, color="gray", alpha=0.3)
    # plt.plot(timesteps, mean_rewards, label=f'Srednia nagroda')
    # plt.plot(timesteps, std_rewards, label=f'Std')

    plt.xlabel("Krok czasowy")
    # plt.ylabel('Średnia nagroda')
    # plt.title('Krzywe uczenia dla różnych zestawów hiperparametrów')
    plt.legend()
    plt.savefig(f"set {i}.png")
