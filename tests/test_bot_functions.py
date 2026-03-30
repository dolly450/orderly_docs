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
    """Test that _send_chat handles Claude CLI errors and returns the quota limit message."""
    mock_proc = AsyncMock()
    mock_proc.returncode = 1
    mock_proc.communicate = AsyncMock(return_value=(b"", b"Error: ratelimit"))

    with patch("asyncio.create_subprocess_exec", return_value=mock_proc), \
         patch("subprocess.run") as mock_run, \
         patch("asyncio.to_thread", return_value=""), \
         patch("bot.get_quota_string", return_value="\n\n=== Claude API Quota Usage ==="), \
         patch("bot._save_session"):
        mock_run.return_value.stdout = "abc123\n"
        bot._session_id = "test-session-123"
        bot._session_start = None
        response = asyncio.run(bot._send_chat("testuser", "Trigger error"))

    assert "⚠️ Claude CLI error" in response
    assert "=== Claude API Quota Usage ===" in response

def test_idea_command_logic():
    mock_vm = Mock()
    user_name = "testuser"
    text = "Great new idea"
    
    result = bot.process_idea_command(mock_vm, text, user_name)
    assert result == "💡 Idea added!"
    mock_vm.write_to_vault.assert_called_once_with("meta/idea-dump", text, user_name)

def test_question_command_logic():
    mock_vm = Mock()
    user_name = "testuser"
    text = "What is the meaning of life?"
    
    result = bot.process_question_command(mock_vm, text, user_name)
    assert result == "❓ Question added!"
    mock_vm.write_to_vault.assert_called_once_with("meta/open-questions", text, user_name)

def test_poll_command_logic():
    mock_vm = Mock()
    user_name = "testuser"
    text = "Is Python the best?"
    
    result = bot.process_poll_command(mock_vm, text, user_name)
    assert result == "📊 Poll added!"
    mock_vm.write_to_vault.assert_called_once_with("meta/polls", text, user_name)
