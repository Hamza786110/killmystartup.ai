import sys


def get_startup_idea() -> str:
    """
    Get the startup idea from the command line if provided
    otherwise prompt the user to type it in.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()

    print("Describe your startup idea:")
    idea = input("> ").strip()
    while not idea:
        print("Please enter a non-empty idea.")
        idea = input("> ").strip()
    return idea