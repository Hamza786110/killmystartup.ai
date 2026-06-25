import sys
from idea_Analyzer import analyze_idea
from Market_Killer import analyze_market
from Competition_Killer import analyze_competition
from Scoring_Agent import score_startup


def get_startup_idea() -> str:
    """
    Get the idea from the command line if provided (e.g.
    `python main.py "AI chatbot platform for ecommerce stores"`),
    otherwise prompt for it interactively.
    """
    if len(sys.argv) > 1:
        return " ".join(sys.argv[1:]).strip()

    print("Describe your startup idea:")
    idea = input("> ").strip()
    while not idea:
        print("Please enter a non-empty idea.")
        idea = input("> ").strip()
    return idea


def run_pipeline(startup_idea: str) -> dict:
    """Run all four steps and return every stage's output (not just the final report)."""
    print("\nStep 1/4: Analyzing idea...")
    idea_output = analyze_idea(startup_idea)

    print("Step 2/4: Analyzing market...")
    market_output = analyze_market(idea_output)

    print("Step 3/4: Analyzing competition...")
    competition_output = analyze_competition(idea_output, market_output)

    print("Step 4/4: Scoring startup...")
    final_report = score_startup(idea_output, market_output, competition_output)

    return {
        "idea_output": idea_output,
        "market_output": market_output,
        "competition_output": competition_output,
        "final_report": final_report,
    }


def print_results(results: dict) -> None:
    """Print every stage of the pipeline, in order."""
    print("\n" + "=" * 70)
    print("STARTUP PROFILE")
    print("=" * 70)
    for key, value in results["idea_output"].items():
        print(f"{key}: {value}")

    print("\n" + "=" * 70)
    print("MARKET ANALYSIS")
    print("=" * 70)
    print(results["market_output"]["messages"][-1].content)

    print("\n" + "=" * 70)
    print("COMPETITION ANALYSIS")
    print("=" * 70)
    print(results["competition_output"]["messages"][-1].content)

    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)
    print(results["final_report"])


if __name__ == "__main__":
    startup_idea = get_startup_idea()

    results = run_pipeline(startup_idea)

    print_results(results)