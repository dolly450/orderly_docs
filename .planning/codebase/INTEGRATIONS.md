# Integrations

## External APIs
- **Discord API**: Connected via WebSocket (Gateway) and Webhooks (Followups). Uses a persistent connection for bot operation, monitoring messages and slash commands.
- **OpenClaw LLM**: Local process integration via `asyncio.create_subprocess_exec` executing the `openclaw ask` CLI command. Acts as the brain for the `#chat` channel.

## Databases (File-Based Vault)
- **Local Filesystem & Git**: Acting as the primary database, the bot writes directly to `.md` files reflecting an Obsidian vault strategy. Data is pushed to GitHub via `GitPython`. The repository `dolly450/orderly_docs` is essentially the remote datastore.

## Auth Providers
- **Discord Token**: Authentication happens via a static bot token in `.env`.
