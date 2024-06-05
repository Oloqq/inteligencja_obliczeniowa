from pettingzoo.butterfly import cooperative_pong_v5
import gymnasium as gym

# from stable_baselines.common.atari_wrappers import make_atari

from stable_baselines3 import DQN


def main():
    env = cooperative_pong_v5.env()
    model1, model2 = None, None
    model1 = DQN("MlpPolicy", env, verbose=1)
    model2 = DQN("MlpPolicy", env, verbose=1)
    timesteps = 100
    model1.learn(timesteps)
    # model2.learn(timesteps)
    # play(env, model1, model2, 10000)


def play(env, model1, model2, maxmoves):
    move = 0
    oo = []
    observations, infos = env.reset()
    while env.agents and move < maxmoves:
        # this is where you would insert your policy
        actions = {agent: env.action_space(agent).sample() for agent in env.agents}
        # print(actions)

        paddle0 = observations["paddle_0"]
        paddle1 = observations["paddle_1"]
        observations, rewards, terminations, truncations, infos = env.step(actions)
        # oo.append(observations)

        move += 1

    # with open("bruh.txt", "w") as f:
    #     for o in oo:
    #         f.write(str(o) + "\n")
    env.close()


main()
