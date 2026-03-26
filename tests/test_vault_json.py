import pytest
import os
import json
import shutil
from vault_manager import VaultManager

@pytest.fixture
def temp_vault(tmp_path):
    # Create a dummy git repo for VaultManager
    vault_dir = tmp_path / "vault"
    vault_dir.mkdir()
    
    # Initialize a git repo
    import subprocess
    subprocess.run(["git", "init"], cwd=vault_dir)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=vault_dir)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=vault_dir)
    
    # Create a dummy remote
    remote_dir = tmp_path / "remote"
    remote_dir.mkdir()
    subprocess.run(["git", "init", "--bare"], cwd=remote_dir)
    subprocess.run(["git", "remote", "add", "origin", str(remote_dir)], cwd=vault_dir)
    
    # Mocking _commit_and_push to avoid actual push in tests (too complex to setup dummy remote push)
    with pytest.MonkeyPatch().context() as m:
        m.setattr(VaultManager, "_commit_and_push", lambda self, msg: None)
        yield VaultManager(str(vault_dir))

def test_write_poll_creates_json(temp_vault):
    poll_id = "poll123"
    text = "Is this a test?"
    author = "tester"
    
    temp_vault.write_poll(poll_id, text, author)
    
    filepath = os.path.join(temp_vault.vault_path, "meta/polls.json")
    assert os.path.exists(filepath)
    
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    assert poll_id in data
    assert data[poll_id]["text"] == text
    assert data[poll_id]["author"] == author
    assert data[poll_id]["votes"] == []

def test_add_vote_updates_json(temp_vault):
    poll_id = "poll123"
    temp_vault.write_poll(poll_id, "Test", "author")
    
    temp_vault.add_vote(poll_id, "user1")
    temp_vault.add_vote(poll_id, "user2")
    temp_vault.add_vote(poll_id, "user1") # Duplicate vote
    
    filepath = os.path.join(temp_vault.vault_path, "meta/polls.json")
    with open(filepath, 'r') as f:
        data = json.load(f)
    
    assert "user1" in data[poll_id]["votes"]
    assert "user2" in data[poll_id]["votes"]
    assert len(data[poll_id]["votes"]) == 2

def test_archive_poll_moves_to_decisions(temp_vault):
    poll_id = "poll123"
    temp_vault.write_poll(poll_id, "Highly controversial poll", "tester")
    temp_vault.add_vote(poll_id, "u1")
    temp_vault.add_vote(poll_id, "u2")
    temp_vault.add_vote(poll_id, "u3")
    temp_vault.add_vote(poll_id, "u4")
    
    # Archive poll
    temp_vault.archive_poll(poll_id)
    
    # Check polls.json
    with open(os.path.join(temp_vault.vault_path, "meta/polls.json"), 'r') as f:
        polls = json.load(f)
    assert poll_id not in polls
    
    # Check decisions.md (as specified in plan)
    decisions_path = os.path.join(temp_vault.vault_path, "meta/decisions.md")
    with open(decisions_path, 'r') as f:
        content = f.read()
    assert "[tester] Approved Poll: Highly controversial poll" in content
