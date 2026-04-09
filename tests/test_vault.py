import pytest
import os
from vault_manager import VaultManager

# Mocking Git for testing purposes (optional for local checks)
def test_vault_write():
    vault_path = "."
    vm = VaultManager(vault_path)
    
    topic = "meta/test-topic"
    content = "This is a test idea"
    user_name = "TestUser"
    
    # 1. Καθαρίζουμε το αρχείο αν υπάρχει
    file_path = os.path.join(vault_path, "meta/test-topic.md")
    if os.path.exists(file_path):
        os.remove(file_path)
        
    # 2. Γράφουμε μια νέα ιδέα
    vm.write_to_vault(topic, content, user_name)
    
    # 3. Ελέγχουμε αν το αρχείο δημιουργήθηκε και αν έχει το σωστό περιεχόμενο
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        data = f.read()
        assert f"[{user_name}] {content}" in data
        
    print("VaultManager Write Test PASSED!")
