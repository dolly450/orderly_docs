import os
from git import Repo
import logging

logger = logging.getLogger('VaultManager')

class VaultManager:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.repo = Repo(vault_path)

    def write_to_vault(self, topic, content, user_name, mode='a'):
        # Καθαρισμός του topic για το όνομα του αρχείου
        filename = f"{topic.lower().replace(' ', '-')}.md"
        file_path = os.path.join(self.vault_path, filename)
        
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"# {topic.title()}\n\n")

        formatted_content = f"- [{user_name}] {content}"

        with open(file_path, mode) as f:
            f.write(formatted_content + "\n")
        
        commit_msg = f"Update {topic} by {user_name}: {content[:30]}..."
        self._commit_and_push(commit_msg)
        return f"Successfully updated {topic}!"

    def read_from_vault(self, topic):
        filename = f"{topic.lower().replace(' ', '-')}.md"
        file_path = os.path.join(self.vault_path, filename)
        
        if not os.path.exists(file_path):
            return f"Topic '{topic}' is currently empty."
            
        with open(file_path, 'r') as f:
            return f.read()

    def _commit_and_push(self, message):
        try:
            self.repo.git.add(A=True)
            self.repo.index.commit(message)
            origin = self.repo.remote(name='origin')
            # Χρησιμοποιούμε force-push αν χρειαστεί, αλλά για τώρα κανονικό push
            origin.push()
            logger.info(f"Git push successful: {message}")
        except Exception as e:
            logger.error(f"Git error: {e}")
