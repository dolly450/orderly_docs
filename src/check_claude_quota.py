#!/usr/bin/env python3
import os
import json
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

def format_reset_time(iso_time: str) -> str:
    """Format ISO timestamp to human-readable relative time"""
    if not iso_time:
        return "N/A"
    try:
        reset_dt = datetime.fromisoformat(iso_time.replace('Z', '+00:00'))
        now = datetime.now(reset_dt.tzinfo)
        delta = reset_dt - now

        if delta.total_seconds() < 0:
            return "Now"

        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes = remainder // 60
        return f"{hours}h {minutes}m" if hours > 0 else f"{minutes}m"
    except Exception:
        return iso_time

def get_claude_token() -> str:
    paths = [
        Path.home() / ".claude" / ".credentials.json",
        Path.home() / ".claude" / "credentials.json",
        Path.home() / ".config" / "claude" / "credentials.json",
    ]
    for p in paths:
        if p.exists():
            try:
                creds = json.loads(p.read_text())
                if "claudeAiOauth" in creds:
                    return creds["claudeAiOauth"].get("accessToken")
                return creds.get("accessToken")
            except Exception:
                pass
    return os.environ.get("CLAUDE_ACCESS_TOKEN", "")

def get_quota_reset_datetime() -> datetime | None:
    """Return the UTC datetime when the quota resets, or None if unknown."""
    token = get_claude_token()
    if not token:
        return None

    url = "https://api.anthropic.com/api/oauth/usage"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": "oauth-2025-04-20"
    })
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            reset_str = None
            if "five_hour" in data and data["five_hour"] and data["five_hour"].get("utilization", 0) >= 99:
                reset_str = data["five_hour"].get("resets_at")
            if not reset_str and "seven_day" in data and data["seven_day"] and data["seven_day"].get("utilization", 0) >= 99:
                reset_str = data["seven_day"].get("resets_at")
            if reset_str:
                dt = datetime.fromisoformat(reset_str.replace('Z', '+00:00'))
                return dt.replace(tzinfo=None)  # Convert to naive UTC to match datetime.utcnow()
    except Exception:
        pass
    # If API fails or we can't parse, fallback to None
    return None

def get_quota_string() -> str:
    token = get_claude_token()
    if not token:
        return "Error: Could not find Claude API token from ~/.claude/.credentials.json"

    url = "https://api.anthropic.com/api/oauth/usage"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "anthropic-beta": "oauth-2025-04-20"
    })

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            
            lines = ["=== Claude API Quota Usage ==="]
            if "five_hour" in data and data["five_hour"]:
                five = data["five_hour"]
                lines.append("5-Hour Window:")
                lines.append(f"  Used:      {five.get('utilization', 0):.1f}%")
                lines.append(f"  Remaining: {100 - five.get('utilization', 0):.1f}%")
                lines.append(f"  Resets in: {format_reset_time(five.get('resets_at'))}")
                
            if "seven_day" in data and data["seven_day"]:
                seven = data["seven_day"]
                lines.append("\n7-Day Window:")
                lines.append(f"  Used:      {seven.get('utilization', 0):.1f}%")
                lines.append(f"  Remaining: {100 - seven.get('utilization', 0):.1f}%")
                lines.append(f"  Resets in: {format_reset_time(seven.get('resets_at'))}")
                
            if not data.get("five_hour") and not data.get("seven_day"):
                lines.append("No usage data returned by Anthropics API (Quota might not be active).")
                lines.append(json.dumps(data, indent=2))
            
            return "\n".join(lines)
                
    except urllib.error.HTTPError as e:
        return f"HTTP Error {e.code}: {e.read().decode('utf-8')}"
    except Exception as e:
        return f"Error checking quota: {e}"

def check_quota():
    print(get_quota_string())

if __name__ == "__main__":
    check_quota()
