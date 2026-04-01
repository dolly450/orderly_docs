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

    def write_idea_poll(self, idea_id, text, user_name):
        ideas_dir = os.path.join(self.vault_path, "meta/ideas")
        os.makedirs(ideas_dir, exist_ok=True)
        
        file_path = os.path.join(ideas_dir, f"{idea_id}.md")
        
        import yaml
        
        data = {
            "id": idea_id,
            "author": user_name,
            "votes": 0,
            "voters": [],
            "created_at": datetime.datetime.now().isoformat(),
            "status": "active"
        }
        
        content = f"---\n{yaml.dump(data, default_flow_style=False, sort_keys=False)}---\n# Idea\n{text}\n"
        
        with open(file_path, 'w') as f:
            f.write(content)
            
        self._commit_and_push(f"Add idea {idea_id} by {user_name}")
        return f"Idea {idea_id} added to vault."

    def add_idea_vote(self, idea_id, user_id):
        file_path = os.path.join(self.vault_path, "meta/ideas", f"{idea_id}.md")
        if not os.path.exists(file_path):
            return False
            
        import yaml
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        if not content.startswith("---"): return False
        
        parts = content.split("---", 2)
        if len(parts) < 3: return False
        
        frontmatter = parts[1]
        md_content = parts[2]
        
        try:
            data = yaml.safe_load(frontmatter)
        except:
            return False
            
        if user_id not in data.get("voters", []):
            if "voters" not in data:
                data["voters"] = []
            data["voters"].append(user_id)
            data["votes"] = len(data["voters"])
            
            new_frontmatter = yaml.dump(data, default_flow_style=False, sort_keys=False)
            new_content = f"---\n{new_frontmatter}---{md_content}"
            
            with open(file_path, 'w') as f:
                f.write(new_content)
                
            self._commit_and_push(f"Vote on idea {idea_id} by {user_id}")
            return True
        return False

    def archive_idea_poll(self, idea_id):
        file_path = os.path.join(self.vault_path, "meta/ideas", f"{idea_id}.md")
        if not os.path.exists(file_path):
            return False
            
        import yaml
        
        with open(file_path, 'r') as f:
            content = f.read()
            
        if not content.startswith("---"): return False
        
        parts = content.split("---", 2)
        if len(parts) < 3: return False
        
        frontmatter = parts[1]
        md_content = parts[2]
        
        data = yaml.safe_load(frontmatter)
        
        # Mark as approved
        data["status"] = "approved"
        new_frontmatter = yaml.dump(data, default_flow_style=False, sort_keys=False)
        new_content = f"---\n{new_frontmatter}---{md_content}"
        
        with open(file_path, 'w') as f:
            f.write(new_content)
            
        # Add to decisions.md
        idea_text = md_content.replace("# Idea", "").strip()
        self.write_to_vault("meta/decisions", f"Approved Idea: {idea_text}", data.get('author', 'Unknown'))
        
        self._commit_and_push(f"Archive approved idea {idea_id}")
        return True

    def get_active_ideas(self):
        ideas_dir = os.path.join(self.vault_path, "meta/ideas")
        if not os.path.exists(ideas_dir):
            return "No active ideas."
            
        import yaml
        
        active_ideas = []
        for filename in os.listdir(ideas_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(ideas_dir, filename)
                with open(file_path, 'r') as f:
                    content = f.read()
                
                if content.startswith("---"):
                    parts = content.split("---", 2)
                    if len(parts) >= 3:
                        try:
                            data = yaml.safe_load(parts[1])
                            idea_text = parts[2].replace("# Idea", "").strip()
                            if data.get("status") == "active":
                                votes = data.get("votes", 0)
                                author = data.get("author", "Unknown")
                                active_ideas.append((data["id"], author, idea_text, votes))
                        except:
                            pass
                            
        if not active_ideas:
            return "No active ideas."
            
        content_lines = []
        for i_id, i_author, i_text, i_votes in active_ideas:
            content_lines.append(f"- {i_text} (by {i_author}) - 📈 {i_votes}/4 votes")
            
        return "\n".join(content_lines)

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
