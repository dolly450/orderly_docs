import pytest
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import bot

def test_generate_ai_response():
    """Test that _send_chat calls the opencode HTTP API correctly."""
    import aiohttp
    
    mock_response_data = [
        {"role": "assistant", "parts": [{"type": "text", "text": "This is the AI response."}]}
    ]
    
    # Mock aiohttp.ClientSession
    mock_resp = AsyncMock()
    mock_resp.status = 200
    mock_resp.json = AsyncMock(return_value=mock_response_data)
    mock_resp.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_resp.__aexit__ = AsyncMock(return_value=False)
    
    mock_post = AsyncMock()
    mock_post.__aenter__ = AsyncMock(return_value=mock_resp)
    mock_post.__aexit__ = AsyncMock(return_value=False)
    
    mock_session = AsyncMock()
    mock_session.__aenter__ = AsyncMock(return_value=mock_session)
    mock_session.__aexit__ = AsyncMock(return_value=False)
    mock_session.post = Mock(return_value=mock_post)
    
    with patch('aiohttp.ClientSession', return_value=mock_session):
        # Set a session ID for the test
        bot._session_id = "test-session-123"
        response = asyncio.run(bot._send_chat("testuser", "What is our plan?"))

    assert response == "This is the AI response."

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
