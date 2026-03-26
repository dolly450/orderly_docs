# Testing

## Framework & Structure
- **Framework**: Standard `pytest` testing ecosystem.
- **Directories**: All tests sit isolated in the root `tests/` path.
- **Asynchronous Tests**: The project does NOT utilize `pytest.mark.asyncio`. All asynchronous logic is evaluated purely by wrapping coroutines via manual `asyncio.run()` in the test block.

## Mocking Strategy
- **Discord Mocking**: Discord objects (`discord.Interaction`, `discord.Message`, `discord.User`, etc.) are heavily mocked using `unittest.mock.Mock`. No real Discord connection occurs during CI tests.
- **Vault Abstraction**: `VaultManager` functionality (`VaultManager.read_from_vault`) is completely mocked inside logic validation scripts to emulate state injections without causing test-side git complications.
- **Subprocess Mocking**: Uses `unittest.mock.AsyncMock` patched across `asyncio.create_subprocess_exec` to fake the OpenClaw AI LLM replies without creating computational overhead locally.
