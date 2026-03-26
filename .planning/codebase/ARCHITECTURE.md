# Architecture

## Key Patterns
The application follows a modular monolith approach utilizing background processing to decouple network and I/O bottlenecks.

- **Event-Driven UI**: Discord handles the presentation layer through slash commands (`/idea`, `/question`, `/poll`) and reaction events.
- **Async I/O Offloading**: Heavy synchronous tasks (e.g. Git pushing) are offloaded to background threads using `asyncio.to_thread()`, keeping the primary Discord WebSocket responsive.
- **Sync/Async Boundary**: `src/bot.py` is fully async (Discord event loop), while `src/vault_manager.py` is strictly synchronous.

## Layers & Components
1. **Discord Presentation Layer (`src/bot.py`)**
   - Handles gateway events, authenticates commands, constructs interaction responses, and reads/pins files to channels.
2. **AI Processing Node**
   - Intercepts messages in `#chat`, aggregates content from various markdown files contextually, and sub-processes an LLM CLI (`openclaw`) to return a natural language response.
3. **Storage Abstraction (`src/vault_manager.py`)**
   - Formats input, ensures markdown directories exist, appends line items, and fires the `git commit` and `git push` network events.

## Data Flow
**Incoming Idea Request**: Discord User -> `/idea interaction` -> `bot.py` async handle -> `asyncio.to_thread` -> `VaultManager.write_to_vault` (appends text, commits, pushes). Discord interactions are deferred early and followed-up asynchronously.
