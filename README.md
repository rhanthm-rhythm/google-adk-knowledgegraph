# Google ADK — Knowledge Graph Examples

This repository contains example agents and helpers that demonstrate using the Google ADK (Agents Development Kit)
with a Neo4j-backed knowledge graph. It's intended as a developer playground: run Neo4j locally with Docker,
start the ADK web UI, and try the sample agents included in `agent/`, `knowledge_graph_agent/`, and `stateful_agent/`.

## Contents

- `agent/` — example agent definitions and a small runner.
- `knowledge_graph_agent/` — an alternative agent layout and test harnesses.
- `stateful_agent/` — another agent variant using session/state helpers.
- `data/`, `logs/` — local Neo4j database folders (ignored by git).
- `requirements.txt`, `pyproject.toml` — Python dependencies.

## Prerequisites

- Docker and Docker Compose (for Neo4j)
- Python 3.10+ and virtualenv (recommended)
- A Google ADK-compatible API key and configuration (set via `.env` — see Environment)

## Quick start (recommended)

1. Start Neo4j (from repository root):

```powershell
docker compose up -d
```

2. Create and activate an environment:

	**Option A — Astral uv (recommended if you already use uv):**

	```powershell
	uv venv --python 3.13.9
    .venv\Scripts\activate.ps1 # for windows
	# Choose one of the following commands to install dependencies:
	uv add -r requirements.txt            # adds packages to uv-managed metadata
	# or
	uv pip install -r requirements.txt    # installs without modifying metadata
	uv run python --version   # sanity-check the interpreter
	```

	uv automatically uses the `.venv` folder by default. When using `uv run <cmd>` you do not
	need to activate the environment manually; uv will run the command inside the managed venv.

	**Option B — Standard `venv`:**

	```powershell
	python -m venv .venv
	& .\.venv\\Scripts\\Activate.ps1
	pip install -r requirements.txt
	```

3. Configure environment variables. Create a `.env` file in the repo root with the following keys (example):

```ini
# .env
GOOGLE_API_KEY=your_api_key_here
GOOGLE_GENAI_USE_VERTEXAI=false
```

5. Start the ADK web UI (optional, useful for interactive debugging):

```powershell
adk web --host 127.0.0.1 --port 8000
```

## Running the example runner

The primary example runner is `agent/runner.py`. It is written as an async script and is runnable directly:

```powershell
& .\.venv\Scripts\Activate.ps1    # if not already active
python -u agent\runner.py
```

This script initializes an in-memory session, builds a `Runner` around the `root_agent`, and demonstrates
calling sub-agents via a small helper. The repo includes a minimal `agent/helper.py` stub so the runner works
out of the box; replace that stub with your full integration as needed.

## Running tests / test harness

There is a small test harness in `knowledge_graph_agent/tests/test1.py`. It expects the package layout to be
importable from the repository root. Run it like this:

```powershell
& .\.venv\Scripts\Activate.ps1
python -u knowledge_graph_agent\tests\test1.py
```

If you see `ModuleNotFoundError` for `knowledge_graph_agent`, ensure you run the script from the repo root so
Python can resolve the package imports.

## Environment and secrets

- Put sensitive keys and configuration in `.env` (already ignored by `.gitignore`).
- The repository ignores local Neo4j data (`data/` and `logs/`) and Python caches.

## Troubleshooting

- Module import errors (e.g. `ModuleNotFoundError` for `knowledge_graph_agent`):
	- Ensure you run scripts from the repository root (so local packages are on `sys.path`).
	- Check for typos in imports (for example `knowlegde_graph_agent` vs `knowledge_graph_agent`).

- `agent.helper` or ADK integration missing:
	- A minimal `agent/helper.py` stub is included to let the runner work. Replace it with your production helper
		that integrates with your ADK session and authentication model.

- Neo4j connection problems:
	- Confirm Docker containers are running: `docker ps` and `docker compose logs neo4j`.
	- If Neo4j is bound to a non-default port, update any connection configuration accordingly.

## Contributing

Feel free to open an issue or submit a PR. If you add persistent files or large model caches, add them to `.gitignore`.

## License
