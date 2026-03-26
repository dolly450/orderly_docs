import pytest
import os
import asyncio
from unittest.mock import Mock, patch, AsyncMock
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import bot

def test_generate_ai_response():
    # Mock vault manager
    mock_vm = Mock()
    mock_vm.read_from_vault.return_value = "Mocked Vault Content"
    
    # Mock subprocess
    mock_process = AsyncMock()
    mock_process.communicate.return_value = (b"This is the AI response.", b"")
    mock_process.returncode = 0
    
    with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_exec:
        OPENCLAW_CMD = os.getenv('OPENCLAW_PATH', '/home/harold/.bun/bin/openclaw')
        
        response = asyncio.run(bot.get_ai_response(mock_vm, "testuser", "What is our plan?"))
        
        assert response == "This is the AI response."
        mock_exec.assert_called_once()
        args = mock_exec.call_args[0]
        assert args[0] == OPENCLAW_CMD
        assert args[1] == 'ask'
        assert "User (@testuser) asks: What is our plan?" in args[2]

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
