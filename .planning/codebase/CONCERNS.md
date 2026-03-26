# Concerns & Tech Debt

## Security
- **Token Handling**: Standard usage of `.env` limits exposure.
- **Shell Injection**: Subprocessing the `openclaw ask` CLI relies on injecting `message.content` broadly into the prompt variable strings. While discord limits string mechanics naturally, there is lack of strict prompt sanitization.

## Data & Vault Fragility
- **Git Merge Conflicts**: The most critical flaw internally right now. `VaultManager` executes `git add .`, `commit`, and `push`. However, if another contributor natively updates the Markdown files in the GitHub repo, the bot lacks a standard `git fetch && git rebase` loop. Upon next push, Git will decline the network flow via a `failed to push some refs`, permanently crippling the bot until manual intervention.
- **File System Locking**: With concurrent background updates (`update_all_channels`) and incoming slash commands, there are overlapping reads/writes. Standard `with open(..., 'a')` is mostly forgiving, but race conditions mapping to the same markdown note simultaneously might corrupt file output.

## Technical Debt
- **Pagination & Vault Limits**: Reading entire files to push context to the AI via `.read().[:300]` is highly rudimentary. As vault files scale to thousands of lines, this primitive trimming and lack of RAG retrieval will cause Hallucinations and OOM context limits.
- **Discord Pin Limitations**: Discord limits Pins to 50 per channel. The bot assumes modifying its single existing pin prevents this, however, if users aggressively pin content, the bot's pin process (`silent_update_channel`) could raise HTTP 400 Bad Requests if the channel cap is hit before finding its existing Pin message.
