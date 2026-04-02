import pytest
from unittest.mock import MagicMock, patch
from vault_manager import VaultManager

def test_sync_repo_calls_pull_rebase():
    # Mock the Repo object
    with patch('vault_manager.Repo') as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_origin = MagicMock()
        mock_repo_instance.remote.return_value = mock_origin
        
        vm = VaultManager("/tmp/fake-vault")
        
        # Action
        vm.sync_repo()
        
        # Verify
        mock_repo_instance.remote.assert_called_with(name='origin')
        mock_origin.pull.assert_called_once_with(rebase=True)

def test_sync_repo_handles_exception():
    with patch('vault_manager.Repo') as MockRepo:
        mock_repo_instance = MockRepo.return_value
        mock_origin = MagicMock()
        mock_origin.pull.side_effect = Exception("Git pull failed")
        mock_repo_instance.remote.return_value = mock_origin
        
        vm = VaultManager("/tmp/fake-vault")
        
        # This should handle the exception internally and log it (we check it doesn't crash)
        try:
            vm.sync_repo()
            success = True
        except Exception:
            success = False
            
        assert success is True
