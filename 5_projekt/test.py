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
        env = DummyVecEnv([lambda: env])
        env = VecMonitor(env)
        model = SAC("MlpPolicy", env, **hyperparams, verbose=0)
        model.learn(total_timesteps=num_timesteps)
        
        obs = env.reset()
        rewards = []
        for _ in range(num_timesteps):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, info = env.step(action)
            rewards.append(reward[0])  # Upewnij się, że dodajesz jednowymiarowe wartości
            if done.any():
                obs = env.reset()
        
        all_rewards.append(rewards)
        env.close()
    
    all_rewards = np.array(all_rewards)
    mean_rewards = np.mean(all_rewards, axis=0)
    std_rewards = np.std(all_rewards, axis=0)
    
    return mean_rewards, std_rewards

# Definiowanie hiperparametrów
hyperparams_list = [
    {'learning_rate': 0.0003, 'gamma': 0.99},
    {'learning_rate': 0.0001, 'gamma': 0.95},
    {'learning_rate': 0.0005, 'gamma': 0.99},
]

env_name = "Pendulum-v1"
num_timesteps = 100

# Trenowanie i zbieranie nagród dla różnych zestawów hiperparametrów
results = []
for hyperparams in hyperparams_list:
    mean_rewards, std_rewards = train_and_evaluate(env_name, hyperparams, num_timesteps)
    results.append((mean_rewards, std_rewards))

# Rysowanie wykresu
timesteps = np.arange(num_timesteps)
plt.figure(figsize=(14, 7))

for i, (mean_rewards, std_rewards) in enumerate(results):
    plt.plot(timesteps, mean_rewards, label=f'Set {i+1}')

plt.xlabel('Krok czasowy')
plt.ylabel('Średnia nagroda')
plt.title('Krzywe uczenia dla różnych zestawów hiperparametrów')
plt.legend()
plt.show()
