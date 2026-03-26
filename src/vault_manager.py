import os
import json
from git import Repo
import logging
import datetime

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

    def write_poll(self, poll_id, text, user_name):
        file_path = os.path.join(self.vault_path, "meta/polls.json")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        data = {}
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
        
        data[poll_id] = {
            "text": text,
            "author": user_name,
            "votes": [],
            "created_at": datetime.datetime.now().isoformat()
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        self._commit_and_push(f"Add poll {poll_id} by {user_name}")
        return f"Poll {poll_id} added to vault."

    def add_vote(self, poll_id, user_id):
        file_path = os.path.join(self.vault_path, "meta/polls.json")
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if poll_id not in data:
            return False
            
        if user_id not in data[poll_id]["votes"]:
            data[poll_id]["votes"].append(user_id)
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=4)
            self._commit_and_push(f"Vote on poll {poll_id} by {user_id}")
            return True
        return False

    def archive_poll(self, poll_id):
        file_path = os.path.join(self.vault_path, "meta/polls.json")
        if not os.path.exists(file_path):
            return False
            
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        if poll_id not in data:
            return False
            
        poll = data.pop(poll_id)
        
        # Write back remaining polls
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
            
        # Add to decisions.md
        self.write_to_vault("meta/decisions", f"Approved Poll: {poll['text']}", poll['author'])
        
        self._commit_and_push(f"Archive poll {poll_id}")
        return True

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
