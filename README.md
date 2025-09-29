## Short description
This repository contains an agent-based chatbot and a preprocessing script. The repository does NOT include any data files — you must provide your own data source to run the code.

## Important: provide your own data
- The code expects a JSON data file (the default preprocessor writes `pokemon_data.json`).
- If you want to use your own data, place it under `./data/` or update the path used by the code (see `pre_process.py` and `main.py`).

## Getting started (macOS)
1. Create and activate a virtual environment:
   - python3 -m venv .venv
   - source .venv/bin/activate

2. Install dependencies
   - If using Poetry: `poetry install`
   - If using pip / pyproject-based installer, install needed libs (example):
     - python3 -m pip install -U pip
     - python3 -m pip install requests langchain langchain-community tiktoken
   - Or add dependencies to `pyproject.toml` and install with your tool of choice.

3. Run the preprocessor
   - Using your "uv" runner (if available): `uv run pre_process.py`
   - Or directly with Python: `python3 pre_process.py`

   The default `pre_process.py` fetches Pokemon data from pokeapi.co for IDs 1–100 and writes `pokemon_data.json` in the current working directory. Change the range or filename inside `pre_process.py` if needed.

4. Run the main chatbot
   - Follow README or inspect `main.py` for required environment variables (API keys, DATA_PATH, etc.)
   - Example: `uv run main.py` or `python3 main.py`

## Notes
- Ensure network access for external APIs (e.g., pokeapi.co) when running `pre_process.py`.
- If your environment does not have a `uv` CLI, run scripts with `python3` as shown above.
- Verify `pyproject.toml` contains required dependencies (e.g., `langchain-community`) so token-tracking callbacks work.

## Troubleshooting
- If token counting or callbacks behave unexpectedly, confirm your LangChain version and provider integrations.
