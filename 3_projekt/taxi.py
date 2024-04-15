import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import pickle

def run(episodes, is_training=True, render=False):
    env = gym.make('Taxi-v3', render_mode='human' if render else None)

    if(is_training):
        q = np.zeros((env.observation_space.n, env.action_space.n))
    else:
        f = open('taxi.pkl', 'rb')
        q = pickle.load(f)
        f.close()

    learning_rate_a = 0.9
    discount_factor_g = 0.9
    epsilon = 0.02
    epsilon_decay_rate = 0.001
    rng = np.random.default_rng()

    rewards_per_episode = np.zeros(episodes)

    for i in range(episodes):
        state = env.reset()[0]
        terminated = False
        truncated = False

        while(not terminated and not truncated):
            if is_training and rng.random() < epsilon:
                action = env.action_space.sample() # actions: 0=left,1=down,2=right,3=up
            else:
                action = np.argmax(q[state,:])

            new_state, reward, terminated, truncated, _ = env.step(action)

            if is_training:
                q[state,action] += learning_rate_a * (reward + discount_factor_g * np.max(q[new_state,:]) - q[state,action])
            state = new_state

        epsilon = max(epsilon - epsilon_decay_rate, 0)

        rewards_per_episode[i] = reward

    env.close()

    sum_rewards = np.zeros(episodes)
    for t in range(episodes):
        sum_rewards[t] = np.sum(rewards_per_episode[max(0, t-100):(t+1)])
    plt.plot(sum_rewards)
    plt.savefig('taxi.png')

    if is_training:
        f = open("taxi.pkl","wb")
        pickle.dump(q, f)
        f.close()

if __name__ == '__main__':
    # run(15000)


    # run(100, is_training=False, render=True)
    run(300, is_training=True, render=False)