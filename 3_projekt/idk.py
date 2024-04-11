import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import cv2

class DQNNetwork(nn.Module):
    def __init__(self, input_shape, num_actions):
        super(DQNNetwork, self).__init__()
        self.conv1 = nn.Conv2d(input_shape[0], 32, kernel_size=8, stride=4)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=4, stride=2)
        self.conv3 = nn.Conv2d(64, 64, kernel_size=3, stride=1)
        self.fc = nn.Linear(3136, 512)
        self.out = nn.Linear(512, num_actions)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = torch.relu(self.conv3(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc(x))
        x = self.out(x)
        return x

def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    image = cv2.resize(image, (84, 84))
    return image

env = gym.make("CarRacing-v2")
input_shape = (1, 84, 84)
num_actions = env.action_space.shape[0]

net = DQNNetwork(input_shape, num_actions)
optimizer = optim.Adam(net.parameters(), lr=0.001)
criterion = nn.MSELoss()

num_episodes = 1000
gamma = 0.9  # discount factor
batch_size = 32

for episode in range(num_episodes):
    done = False
    total_reward = 0
    state = preprocess_image(env.reset())
    state = torch.tensor(state, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

    while not done:
        with torch.no_grad():
            q_values = net(state)
        action = torch.argmax(q_values).item()
        next_state, reward, done, _ = env.step(action)
        next_state = preprocess_image(next_state)
        next_state = torch.tensor(next_state, dtype=torch.float32).unsqueeze(0).unsqueeze(0)

        target = reward + gamma * torch.max(net(next_state)).item() * (not done)
        target_q_values = q_values.clone()
        target_q_values[0, action] = target

        loss = criterion(q_values, target_q_values)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        state = next_state
        total_reward += reward

    print(f"Episode {episode+1}: Total Reward: {total_reward}")
