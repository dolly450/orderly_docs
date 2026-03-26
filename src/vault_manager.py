import os
from git import Repo

class VaultManager:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.repo = Repo(vault_path)

    def write_to_vault(self, topic, content, mode='a'):
        # Καθαρισμός του topic για το όνομα του αρχείου
        filename = topic.lower().replace(' ', '-') + '.md'
        file_path = os.path.join(self.vault_path, filename)
        
        # Σιγουρευόμαστε ότι ο φάκελος υπάρχει
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        # Αν το αρχείο δεν υπάρχει, το δημιουργούμε
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"# {topic.title()}\n\n")

        with open(file_path, mode) as f:
            f.write(content + "\n")
        
        # Καλύτερο commit message βασισμένο στο περιεχόμενο
        summary = content.strip().lstrip('-').split('\n')[0][:50]
        commit_msg = f"Update {topic}: {summary}"
        
        self._commit_and_push(commit_msg)
        return f"Successfully updated {topic}! (Git synced)"

    def read_from_vault(self, topic):
        filename = topic.lower().replace(' ', '-') + '.md'
        file_path = os.path.join(self.vault_path, filename)
        
        if not os.path.exists(file_path):
            return f"Topic '{topic}' not found in Vault."
            
        with open(file_path, 'r') as f:
            return f.read()

    def _commit_and_push(self, message):
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(message)
            # Χρησιμοποιούμε force push ή απλό push για να είμαστε σίγουροι
            origin = self.repo.remote(name='origin')
            origin.push()
            print(f"Git push successful: {message}")
        except Exception as e:
            print(f"Git error: {e}")
