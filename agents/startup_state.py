from pydantic import BaseModel, Field


class StartupProfile(BaseModel):
    """Structured extraction of a raw startup idea."""

    profile_name: str = Field(..., description="A short name for the startup.")
    year_founded: int = Field(..., description="Year the startup was/would be founded.")
    description: str = Field(..., description="A brief description of the startup.")
    industry: str = Field(..., description="The industry the startup operates in.")
    target_customer: str = Field(..., description="Primary customer base.")
    problem_statement: list[str] = Field(..., description="The problem(s) the startup solves.")
    proposed_solution: str = Field(..., description="The startup's proposed solution.")
    business_model: str = Field(..., description="How the startup makes money.")
    key_features: list[str] = Field(..., description="Key features / unique selling points.")


class MarketAnalysis(BaseModel):
    """Output of the Market Killer agent."""

    market_score: int = Field(..., ge=0, le=10, description="Market viability score out of 10.")
    key_risks: list[str] = Field(..., description="Market risks identified.")
    questions_for_founder: list[str] = Field(..., description="Challenging questions for the founder.")
    summary: str = Field(..., description="Short summary of the market analysis.")


class CompetitorEntry(BaseModel):
    name: str = Field(..., description="Competitor name.")
    reason: str = Field(..., description="Why this competitor is dangerous.")


class CompetitionAnalysis(BaseModel):
    """Output of the Competition Killer agent."""

    competition_score: int = Field(..., ge=0, le=10, description="Competition threat score out of 10.")
    top_competitors: list[CompetitorEntry] = Field(..., description="Strongest existing competitors.")
    competitor_advantages: list[str] = Field(..., description="Advantages competitors currently hold.")
    switching_cost_risks: list[str] = Field(..., description="Risks related to customer switching costs.")
    questions_for_founder: list[str] = Field(..., description="Challenging questions for the founder.")


class ScoringResult(BaseModel):
    """Output of the Scoring Agent — the final verdict."""

    final_score: int = Field(..., ge=0, le=10, description="Overall viability score out of 10.")
    reasoning: list[str] = Field(..., description="Bullet-point reasoning behind the score.")
    questions_for_founder: list[str] = Field(..., description="Final critical questions for the founder.")


class FullReport(BaseModel):
    """The complete JSON payload returned by the pipeline / API."""

    idea: StartupProfile
    market: MarketAnalysis
    competition: CompetitionAnalysis
    # score_startup() (Scoring_Agent) currently returns a free-text verdict from
    # a conversational agent, not a ScoringResult, so this is typed to match
    # what the function actually produces. If you switch score_startup() to
    # use with_structured_output(ScoringResult) like the other agents, change
    # this back to `ScoringResult`.
    scoring: str