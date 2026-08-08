from Competition_Killer import analyze_competition
from Idea_Analyzer import analyze_idea
from Market_Killer import analyze_market
from Scoring_Agent import score_startup
from startup_state import FullReport


def run_pipeline(startup_idea: str) -> FullReport:
    """Run the full Idea -> Market -> Competition -> Scoring pipeline once."""
    idea_output = analyze_idea(startup_idea)
    market_output = analyze_market(idea_output)
    competition_output = analyze_competition(idea_output, market_output)
    scoring_output = score_startup(idea_output, market_output, competition_output)

    return FullReport(
        idea=idea_output,
        market=market_output,
        competition=competition_output,
        scoring=scoring_output,
    )


if __name__ == "__main__":
    import json
    import sys

    idea = " ".join(sys.argv[1:]).strip()
    if not idea:
        idea = input("Describe your startup idea: ").strip()

    report = run_pipeline(idea)
    print(json.dumps(report.model_dump(), indent=2))