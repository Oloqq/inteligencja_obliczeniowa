""" Registers the gymnasium environments and exports the `gymnasium.make` function.
"""
# Silencing pygame:
import os

# Registering environments:
from gymnasium.envs.registration import register

# Exporting envs:
from minecraft.envs.minecraft_env import MinecraftEnv

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

register(
    id="Minecraft-v0",
    entry_point="minecraft:MinecraftEnv",
)

# Main names:
__all__ = [
    MinecraftEnv.__name__,
]
