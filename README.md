# KillMyStartup.ai 🔪

**Brutally honest, multi-agent startup idea validation — powered by LangGraph.**

KillMyStartup.ai takes your raw startup idea and puts it through a gauntlet of specialized AI agents, each tasked with attacking it from a different angle: market viability, competition, finances, technical feasibility, and legal risk. A Defense Agent then argues back on your idea's behalf, and a final Scoring Agent renders a verdict — so you find out your idea's weaknesses *before* the market does.

---

## How It Works

Your idea is run through a pipeline of orchestrated agents built on **LangGraph**, each backed by a different LLM chosen to fit the nature of its task:

| Agent | Role | Model |
|---|---|---|
| **Idea Analyzer** | Parses and structures the raw startup idea | `qwen3:4b` |
| **Market Killer** | Attacks market size, demand, and timing assumptions | Gemini 2.5 Flash |
| **Competition Killer** | Surfaces existing competitors and differentiation gaps | Groq |
| **Finance Killer** | Stress-tests revenue model, costs, and unit economics | Gemini 2.5 Flash |
| **Technical Killer** | Probes feasibility, complexity, and technical risk | Groq |
| **Legal Killer** | Flags regulatory, compliance, and legal exposure | `deepseek-r1:1.5b` |
| **Defense Agent** | Argues in favor of the idea, countering the "killer" agents | `deepseek-r1:1.5b` |
| **Scoring Agent** | Synthesizes all arguments into a final viability score | `qwen3:4b` |

Local, lightweight models (`qwen3:4b`, `deepseek-r1:1.5b` via Ollama) handle structuring, legal review, defense, and scoring, while **Groq** and **Gemini 2.5 Flash** power the heavier-reasoning "killer" agents — balancing speed, cost, and quality across the pipeline.

---

## Tech Stack

- **[LangGraph](https://github.com/langchain-ai/langgraph)** — multi-agent orchestration
- **[LangChain](https://github.com/langchain-ai/langchain)** — LLM tooling and chaining
- **[Groq](https://groq.com/)** via `langchain-groq` — fast inference for competition & technical analysis
- **[Google Gemini](https://ai.google.dev/)** via `langchain-google-genai` — market & finance analysis
- **[Ollama](https://ollama.com/)** via `langchain-ollama` — local model inference (`qwen3:4b`, `deepseek-r1:1.5b`)
- **[Tavily](https://tavily.com/)** — web search / research augmentation for agents
- **[Streamlit](https://streamlit.io/)** — interactive front-end UI
- **[FastAPI](https://fastapi.tiangolo.com/)** — backend API layer
- **[uv](https://github.com/astral-sh/uv)** — Python dependency and environment management

---

## Getting Started

### Prerequisites

- Python **3.13+**
- [uv](https://github.com/astral-sh/uv) installed
- [Ollama](https://ollama.com/) running locally with `qwen3:4b` and `deepseek-r1:1.5b` pulled
- API keys for **Groq**, **Google AI Studio**, and **Tavily**

### Installation

```bash
git clone https://github.com/<your-username>/killmystartup-ai.git
cd killmystartup-ai
uv sync
```

### Environment Variables

Copy the example env file and add your keys:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY="your-groq-api-key"
GOOGLE_API_KEY="your-google-api-key"
TAVILY_API_KEY="your-tavily-api-key"
```

### Pull local models via Ollama

```bash
ollama pull qwen3:4b
ollama pull deepseek-r1:1.5b
```

### Run the app

**Streamlit UI:**
```bash
uv run streamlit run app.py
```

## AI Output
```bash
output of the ai is still in progress , formating the output in a single strucutred format is still in production
```

## Project Structure

```
killmystartup-ai/
├── .env                  # API keys (not committed)
├── pyproject.toml        # Project metadata & dependencies
├── uv.lock                # Locked dependency versions
├── requirements.txt        # Pip-compatible dependency list
└── README.md
```

---

## Roadmap

- [ ] Add scoring breakdown visualization
- [ ] Support exporting validation reports as PDF
- [ ] Add configurable agent weighting
- [ ] Deploy hosted demo

---

## Contributing

Issues and pull requests are welcome. If you have ideas for new "killer" agents or better model routing, open a discussion!

## License

MIT — see `LICENSE` for details.
