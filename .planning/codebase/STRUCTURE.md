# Repository Structure

## Key Locations

- **`src/`**: Contains the source code.
  - `src/bot.py`: The main discord bot execution script and event router.
  - `src/vault_manager.py`: The Git and File-system operation abstraction module.
  
- **`tests/`**: Contains the test suite enforcing TDD implementation.
  - `tests/test_bot_functions.py`: Tests the non-API specific synchronous and async logic layers of the bot, using Mock.
  - `tests/test_vault.py`: Validates the git-push processes and internal IO mechanics.
  
- **`meta/`, `architecture/`, `design/`, `business/`**: The local Markdown Database instances. Acting as an Obsidian Vault synced with the remote repo. Foundational sources of truth.

- **Root files**:
  - `orderly-bot.service`: Template systemd service specification.
  - `PROJECT_LOG.md`: Developer activity, roadmap planning, and active ideas.
  - `FULL_PROJECT_STATUS.md`: The macro state, handover parameters, and open requirements.

## Naming Conventions
- Data directories and log folders use `kebab-case`.
- Markdown source of truths are title-cased in document but use `kebab-case` naming conventions contextually. 
- Python files are in PEP standard `snake_case`.
