import argparse
from minecraft.tests.test_human import play as human_agent_env
from minecraft.tests.test_random import play as random_agent_env
from minecraft.tests.test_smart import play as smart_agent_env


def _get_args():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument(
        "--mode",
        "-m",
        type=str,
        default="human",
        choices=["human", "random", "smart"],
        help="The execution mode for the game.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="If set, the game will be executed without rendering it.",
    )

    return parser.parse_args()


def main():
    args = _get_args()

    if args.mode == "human":
        human_agent_env()
    elif args.mode == "random":
        random_agent_env(
            audio_on=(not args.quiet), render_mode="human" if not args.quiet else None
        )
    elif args.mode == "smart":
        smart_agent_env(audio_on=False, render_mode="human" if not args.quiet else None)
    else:
        print("Invalid mode!")
