""" Setup of the flappy-bird-gymnasium package.
"""

from typing import List

import setuptools

_VERSION = "0.4.0"

# Short description.
short_description = "A Gymnasium environment for the Flappy Bird game."

# Packages needed for the environment to run.
# The compatible release operator (`~=`) is used to match any candidate version
# that is expected to be compatible with the specified version.
REQUIRED_PACKAGES = [
    "gymnasium",
    "numpy",
    "pygame",
    "matplotlib",
]

# Packages which are only needed for testing code.
TEST_PACKAGES = ["black", "isort", "flake8", "pytest"]  # type: List[str]

# Loading the "long description" from the projects README file.
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="minecraft",
    version=_VERSION,
    description=short_description,
    # Contained modules and scripts:
    packages=setuptools.find_packages(),
    package_data={
        "minecraft": [
            "assets/sprites/*",
            "assets/audio/*",
            "assets/model/*",
        ]
    },
    install_requires=REQUIRED_PACKAGES,
    tests_require=REQUIRED_PACKAGES + TEST_PACKAGES,
    license="MIT License",
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "minecraft = minecraft.cli:main",
        ],
    },
)
