# Codebase Stack

## Languages
- **Python** (Runtime version ~3.14.x)
- Markdown (Obsidian Vault structure for data storage)

## Core Frameworks & Dependencies
- `discord.py` (v2.3+): For Discord Bot integration, Slash Commands, and Webhook responses.
- `GitPython`: For managing `.git` repositories programmatically (committing and pushing).
- `pytest`: For the testing suite (`pytest-asyncio` logic natively via `asyncio.run()`).
- `python-dotenv`: For loading `.env` file environment variables.

## Runtimes & Infrastructure
- **Systemd User Service**: The bot runs as a background persistent process via `orderly-bot.service` using `systemctl --user`.
- Virtual Environment (`venv/`): Local python environment isolation.

## Configuration
- `.env`: Holds secrets like `DISCORD_TOKEN`, `VAULT_PATH`, and `OPENCLAW_PATH`.
- Service File: `orderly-bot.service` defines the PYTHONPATH and execution flow.
