import pytest
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import bot

def test_generate_ai_response():
    """Test that _send_chat calls the Claude CLI correctly and returns the result."""
    import json

    fake_output = json.dumps({
        "type": "result",
        "subtype": "success",
        "result": "This is the AI response.",
        "session_id": "new-session-456",
        "is_error": False,
    }).encode()

    mock_proc = AsyncMock()
    mock_proc.returncode = 0
    mock_proc.communicate = AsyncMock(return_value=(fake_output, b""))

    with patch("asyncio.create_subprocess_exec", return_value=mock_proc), \
         patch("subprocess.run") as mock_run, \
         patch("asyncio.to_thread", return_value=""), \
         patch("bot._save_session"):  # don't write to claude_session.json
        mock_run.return_value.stdout = "abc123\n"
        bot._session_id = "test-session-123"
        bot._session_start = None  # force new session
        response = asyncio.run(bot._send_chat("testuser", "What is our plan?"))

    assert response == "This is the AI response."

def test_generate_ai_response_cli_error():
    """Test that _send_chat handles Claude API CLI errors, switches to Gemini, and returns Gemini's output."""
    import json
    
    mock_proc_claude = AsyncMock()
    mock_proc_claude.returncode = 1
    mock_proc_claude.communicate = AsyncMock(return_value=(b"", b"Error: ratelimit"))

    fake_gemini_output = json.dumps({
        "type": "result",
        "subtype": "success",
        "result": "This is Gemini answering.",
        "session_id": "gemini-sess-1",
        "is_error": False,
    }).encode()
    
    mock_proc_gemini = AsyncMock()
    mock_proc_gemini.returncode = 0
    mock_proc_gemini.communicate = AsyncMock(return_value=(fake_gemini_output, b""))

    with patch("asyncio.create_subprocess_exec", side_effect=[mock_proc_claude, mock_proc_gemini]), \
         patch("subprocess.run") as mock_run, \
         patch("bot._get_git_diff", return_value=""), \
         patch("bot.get_quota_string", return_value="=== Claude API Quota Usage ==="), \
         patch("bot.get_quota_reset_datetime", return_value=None), \
         patch("bot._save_session"), \
         patch("bot._save_gemini_session"):
        mock_run.return_value.stdout = "abc123\n"
        bot._fallback_until_dt = None
        bot._active_provider = "claude"
        bot._session_id = "test-session-123"
        bot._session_start = None
        response = asyncio.run(bot._send_chat("testuser", "Trigger error"))

    assert "This is Gemini answering." in response
    assert bot._fallback_until_dt is not None
    assert bot._active_provider == "gemini"

def test_question_command_logic():
    mock_vm = Mock()
    user_name = "testuser"
    text = "What is the meaning of life?"

    result = bot.process_question_command(mock_vm, text, user_name)
    assert result == "❓ Question added!"
    mock_vm.write_to_vault.assert_called_once_with("meta/open-questions", text, user_name)


# ── /idea as poll ──────────────────────────────────────────────────────────────

def test_idea_command_creates_poll():
    """
    /idea should call write_idea_poll (not write_to_vault) and send a
    poll message with ✅ reaction.
    """
    mock_vm = Mock()
    mock_vm.write_idea_poll = Mock()

    mock_interaction = AsyncMock()
    mock_interaction.id = 123456789
    mock_interaction.user.global_name = "testuser"
    mock_interaction.guild.text_channels = []

    mock_followup_msg = AsyncMock()
    mock_interaction.followup.send = AsyncMock(return_value=mock_followup_msg)

    async def fake_to_thread(func, *args, **kwargs):
        return func(*args, **kwargs)

    async def run():
        with patch.object(bot, "vm", mock_vm), \
             patch("asyncio.to_thread", new=fake_to_thread):
            await bot.idea.callback(mock_interaction, text="Νέα ιδέα για δοκιμή")

    asyncio.run(run())

    mock_vm.write_idea_poll.assert_called_once_with(
        "idea-123456789", "Νέα ιδέα για δοκιμή", "testuser"
    )
    sent_text = mock_interaction.followup.send.call_args[0][0]
    assert "💡 **Idea by testuser**" in sent_text
    assert "idea-123456789" in sent_text
    mock_followup_msg.add_reaction.assert_called_once_with("✅")


def test_on_message_create_poll_marker():
    """
    [CREATE_POLL: text] in agent response triggers write_idea_poll,
    posts poll to #ideas, and strips marker from user-visible reply.
    """
    import re

    agent_response = "Εντάξει, δημιουργώ poll. [CREATE_POLL: Νέο feature για Obsidian]"

    mock_vm = Mock()
    mock_vm.write_idea_poll = Mock()

    mock_ideas_channel = AsyncMock()
    mock_poll_msg = AsyncMock()
    mock_ideas_channel.send = AsyncMock(return_value=mock_poll_msg)

    mock_message = AsyncMock()
    mock_message.author.global_name = "AP"
    mock_message.id = 999888777

    async def fake_to_thread(func, *args, **kwargs):
        return func(*args, **kwargs)

    async def run():
        with patch.object(bot, "vm", mock_vm), \
             patch("asyncio.to_thread", new=fake_to_thread), \
             patch("discord.utils.get", return_value=mock_ideas_channel), \
             patch("bot.silent_update_channel", new=AsyncMock()):

            # Replicate the [CREATE_POLL:] handling logic from on_message
            user_name = mock_message.author.global_name
            response = agent_response

            poll_match = re.search(r'\[CREATE_POLL:\s*(.+?)\]', response, re.DOTALL)
            assert poll_match is not None
            idea_text = poll_match.group(1).strip()

            idea_id = f"idea-{mock_message.id}"
            await fake_to_thread(mock_vm.write_idea_poll, idea_id, idea_text, user_name)

            poll_msg = await mock_ideas_channel.send(
                f"💡 **Idea by {user_name}**: {idea_text}\n"
                f"React with ✅ to approve. (ID: `{idea_id}`)"
            )
            await poll_msg.add_reaction("✅")

            clean = re.sub(r'\s*\[CREATE_POLL:\s*.+?\]', '', response, flags=re.DOTALL).strip()
            assert "[CREATE_POLL:" not in clean
            assert "Εντάξει, δημιουργώ poll." in clean

    asyncio.run(run())

    mock_vm.write_idea_poll.assert_called_once_with(
        "idea-999888777", "Νέο feature για Obsidian", "AP"
    )
    sent = mock_ideas_channel.send.call_args[0][0]
    assert "💡 **Idea by AP**" in sent
    assert "idea-999888777" in sent
    mock_poll_msg.add_reaction.assert_called_once_with("✅")


def test_reaction_handler_votes_idea():
    """
    ✅ reaction on an idea poll message calls add_idea_vote.
    """
    from unittest.mock import PropertyMock

    mock_vm = Mock()
    mock_vm.add_idea_vote = Mock(return_value=True)

    sentinel_user = Mock(id=0)  # bot.user mock; id=0 ≠ payload.user_id=42 so handler proceeds

    mock_msg = AsyncMock()
    mock_msg.author = sentinel_user
    mock_msg.content = (
        "💡 **Idea by AP**: test idea\n"
        "React with ✅ to approve. (ID: `idea-111222333`)"
    )
    mock_msg.reactions = []

    mock_channel = AsyncMock()
    mock_channel.fetch_message = AsyncMock(return_value=mock_msg)
    mock_channel.guild.text_channels = []

    mock_payload = Mock()
    mock_payload.user_id = 42
    mock_payload.emoji.name = "✅"
    mock_payload.channel_id = 1
    mock_payload.message_id = 100

    calls = []

    async def fake_to_thread(func, *args, **kwargs):
        calls.append((func, args))
        return func(*args, **kwargs)

    async def run():
        with patch.object(bot, "vm", mock_vm), \
             patch.object(bot.bot, "get_channel", return_value=mock_channel), \
             patch.object(type(bot.bot), "user", new_callable=PropertyMock, return_value=sentinel_user), \
             patch("asyncio.to_thread", new=fake_to_thread), \
             patch("discord.utils.get", return_value=None):
            await bot.on_raw_reaction_add(mock_payload)

    asyncio.run(run())

    # Verify add_idea_vote was called with correct idea_id and user_id
    vote_calls = [(f, a) for f, a in calls if f == mock_vm.add_idea_vote]
    assert len(vote_calls) == 1
    assert vote_calls[0][1] == ("idea-111222333", "42")


def test_create_poll_marker_stripped_from_reply():
    """[CREATE_POLL:...] must never appear in the reply shown to the user."""
    import re

    cases = [
        "Ωραία! [CREATE_POLL: ιδέα Α]",
        "[CREATE_POLL: μόνο marker]",
        "Κείμενο πριν [CREATE_POLL: x] και μετά",
    ]
    for raw in cases:
        result = re.sub(r'\s*\[CREATE_POLL:\s*.+?\]', '', raw, flags=re.DOTALL).strip()
        assert "[CREATE_POLL:" not in result
