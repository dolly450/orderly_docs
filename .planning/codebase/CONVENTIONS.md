# Conventions

## Code Style & Patterns
- **Asynchronous Execution**: Strict requirement that all network-bound Discord Gateway tasks remain unblocked. Heavy IO tasks (reading/writing to the Disk vault and Git Network) MUST be wrapped in `asyncio.to_thread()`.
- **Command Registration**: Commands are registered through `@bot.tree.command` rather than the legacy `ext.commands` framework.
- **TDD (Test-Driven Development)**: Explicit user requirement to always follow TDD. Before any logic is added to `src/bot.py`, an equivalent synchronous/mocked test must be defined in `tests/test_bot_functions.py` to ensure behavioral driven implementations.

## Error Handling
- **Silenced Failures**: Discord failures (e.g., missing permissions, Git connection drops) are swallowed by `try/except` blocks in command execution, logging to `orderly_bot.log` via `logging` instead of crashing the process.
- **User Intimations**: On exception, the bot replies to the slash command interaction follow-up with a brief "Failed to log due to internal error", preventing Interaction timeouts.
- **Console & File Logging**: `logging.StreamHandler()` and `logging.FileHandler()` both capture `logger.info` and `logger.error` for transparent monitoring via `journalctl` (when run via systemd).
