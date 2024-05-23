import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import EvalCallback
import numpy as np
import matplotlib.pyplot as plt

from stable_baselines3.common.monitor import Monitor


class RewardCallback(EvalCallback):
    def __init__(self, eval_env, *args, **kwargs):
        super().__init__(eval_env, *args, **kwargs)
        self.rewards = []
        self.eval_freq = kwargs.get("eval_freq", 10000)

    def _on_step(self):
        result = super()._on_step()
        if self.n_calls % self.eval_freq == 0:
            print(f"Step: {self.n_calls}, Mean Reward: {self.last_mean_reward}")
            self.rewards.append(self.last_mean_reward)
        return result


def train_with_rewards(env_id, hyperparams, total_timesteps=100000, eval_freq=5000):
    env = Monitor(gym.make(env_id))
    eval_env = Monitor(gym.make(env_id))
    callback = RewardCallback(
        eval_env, eval_freq=eval_freq, n_eval_episodes=10, verbose=1
    )
    model = PPO("MlpPolicy", env, **hyperparams, verbose=1)
    model.learn(total_timesteps=total_timesteps, callback=callback)
    env.close()
    eval_env.close()
    return callback.rewards


# Parameters
env_id = "MountainCarContinuous-v0"
hyperparams_list = [
    {"learning_rate": 0.0003, "n_steps": 2048, "batch_size": 64, "n_epochs": 10},
    # {"learning_rate": 0.0001, "n_steps": 1024, "batch_size": 32, "n_epochs": 5},
    # {"learning_rate": 0.0005, "n_steps": 4096, "batch_size": 128, "n_epochs": 20},
]

# Training and plotting
for i, hyperparams in enumerate(hyperparams_list):
    all_rewards = []
    for _ in range(10):
        rewards = train_with_rewards(env_id, hyperparams)
        all_rewards.append(rewards)

    # Calculate mean and std of rewards across runs
    mean_rewards = np.mean(all_rewards, axis=0)
    std_rewards = np.std(all_rewards, axis=0)

    # Plotting
    plt.figure(figsize=(10, 6))
    plt.plot(mean_rewards, label=f"Set {i+1} Mean Reward")
    plt.fill_between(
        range(len(mean_rewards)),
        mean_rewards - std_rewards,
        mean_rewards + std_rewards,
        alpha=0.2,
    )
    plt.title(f"Learning Curve for Hyperparameter Set {i+1}")
    plt.xlabel("Evaluation Step")
    plt.ylabel("Mean Reward")
    plt.legend()
    plt.savefig("test2.png")
