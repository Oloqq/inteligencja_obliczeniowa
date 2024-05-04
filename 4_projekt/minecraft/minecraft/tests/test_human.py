import gymnasium
import pygame

def play():
    env = gymnasium.make(
        "Minecraft-v0", audio_on=False, render_mode="human", use_lidar=False # FIXME fuck lidar
    )

    steps = 0
    video_buffer = []

    obs = env.reset()
    while True:
        action = 0
        # NOTE controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and (
                event.key == pygame.K_SPACE or event.key == pygame.K_UP
            ):
                action = 1

        obs, _, done, _, info = env.step(action)
        video_buffer.append(obs)

        steps += 1
        # print(
        #     f"Obs: {obs}\n"
        #     f"Action: {action}\n"
        #     f"Score: {info['score']}\n Steps: {steps}\n"
        # )

        if done:
            break

    env.close()

if __name__ == "__main__":
    play()
