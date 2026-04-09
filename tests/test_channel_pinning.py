import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock, MagicMock
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import bot

@pytest.mark.asyncio
async def test_idea_command_updates_dedicated_channel():
    # Setup mocks
    mock_interaction = AsyncMock()
    mock_interaction.guild = MagicMock()
    mock_interaction.channel = MagicMock()
    mock_interaction.channel.name = "general"
    mock_interaction.user.global_name = "test_user"
    mock_interaction.user.name = "test_user"
    
    # Mock followup.send specifically
    mock_interaction.followup = AsyncMock()

    # Dedicated channel in the guild
    mock_ideas_channel = MagicMock()
    mock_ideas_channel.name = "ideas"
    mock_interaction.guild.text_channels = [mock_ideas_channel]

    with patch('bot.vm.write_idea_poll', return_value="💡 Idea added!") as mock_process, \
         patch('bot.silent_update_channel', new_callable=AsyncMock) as mock_silent_update, \
         patch('discord.utils.get', return_value=mock_ideas_channel), \
         patch('bot.bot') as mock_bot_instance:
        
        mock_bot_instance.loop = MagicMock()
        mock_interaction.response = AsyncMock()
        # Call the underlying callback
        await bot.idea.callback(mock_interaction, "Great idea!")
        
        # Check interaction followup
        assert mock_interaction.followup.send.call_count == 1
        
        # Check that silent_update_channel was called with dedicated channel
        mock_silent_update.assert_called_once()
        args, _ = mock_silent_update.call_args
        assert args[0] == mock_ideas_channel
        assert args[1] == "meta/ideas"

@pytest.mark.asyncio
async def test_question_command_updates_dedicated_channel():
    # Setup mocks
    mock_interaction = AsyncMock()
    mock_interaction.guild = MagicMock()
    mock_interaction.channel = MagicMock()
    mock_interaction.channel.name = "chat"
    mock_interaction.user.global_name = "test_user"
    mock_interaction.user.name = "test_user"
    
    mock_interaction.followup = AsyncMock()

    # Dedicated channel in the guild
    mock_questions_channel = MagicMock()
    mock_questions_channel.name = "questions"
    mock_interaction.guild.text_channels = [mock_questions_channel]

    with patch('bot.process_question_command', return_value="❓ Question added!") as mock_process, \
         patch('bot.silent_update_channel', new_callable=AsyncMock) as mock_silent_update, \
         patch('discord.utils.get', return_value=mock_questions_channel), \
         patch('bot.bot') as mock_bot_instance:
        
        mock_bot_instance.loop = MagicMock()
        mock_interaction.response = AsyncMock()
        await bot.question.callback(mock_interaction, "How to fix this?")
        
        mock_interaction.followup.send.assert_called_once_with("❓ Question added!")
        mock_silent_update.assert_called_once()
        args, _ = mock_silent_update.call_args
        assert args[0] == mock_questions_channel
        assert args[1] == "meta/open-questions"
