#!/usr/bin/env python3
"""
Orderly Agent CLI - Αντικαθιστά το openclaw για το Discord bot.
Χρήση: python -m src.agent ask "ερώτηση" [--context "vault context"]
       python -m src.agent --help
"""

import os
import sys
import argparse
import requests
from pathlib import Path

AGENT_DIR = Path(__file__).parent.parent
AGENT_INSTRUCTIONS = AGENT_DIR / "AGENT.md"
VAULT_PATH = os.getenv("VAULT_PATH", str(AGENT_DIR))
OPENCLAW_API_URL = os.getenv("OPENCLAW_API_URL", "http://localhost:18789/api/v1")
OPENCLAW_TOKEN = os.getenv("OPENCLAW_TOKEN", "")


def load_instructions():
    if AGENT_INSTRUCTIONS.exists():
        return AGENT_INSTRUCTIONS.read_text()
    return "You are a helpful AI assistant."


def call_llm(prompt: str, system_prompt: str, full_permissions: bool = False) -> str:
    import subprocess
    
    # Path to opencode binary
    OPENCODE_BIN = "/home/harold/.opencode/bin/opencode"
    
    if not os.path.exists(OPENCODE_BIN):
        return f"Error: opencode binary not found at {OPENCODE_BIN}"

    # Combine system prompt and user prompt
    full_message = f"{system_prompt}\n\n{prompt}"
    
    try:
        # Run opencode ask
        process = subprocess.run(
            [OPENCODE_BIN, "ask", full_message],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        if process.returncode == 0:
            response = process.stdout.strip()
            # If opencode output is empty, check stderr (some tools use it for output)
            if not response:
                response = process.stderr.strip()
            return response if response else "Error: Empty response from opencode"
        else:
            return f"Error running opencode (code {process.returncode}): {process.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "Error: opencode took too long (60s timeout)."
    except Exception as e:
        return f"Error in call_llm: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="Orderly Agent CLI - AI agent για το Discord bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "command",
        nargs="?",
        default="ask",
        choices=["ask", "help"],
        help="Command: ask (default)",
    )
    parser.add_argument("question", nargs="?", help="The question/prompt to answer")
    parser.add_argument(
        "--context", "-c", default="", help="Additional context (e.g., vault content)"
    )
    parser.add_argument(
        "--full-permissions",
        action="store_true",
        help="Enable all tools (read, write, execute)",
    )
    parser.add_argument(
        "--read-only", action="store_true", help="Read-only mode (default)"
    )

    args = parser.parse_args()

    if args.command == "help" or not args.question:
        print(f"""Orderly Agent CLI

Χρήση:
  python -m src.agent ask "ερώτηση" [options]
  python -m src.agent ask "ερώτηση" --context "vault content"
  python -m src.agent ask "ερώτηση" --full-permissions

Επιλογές:
  --context, -c        Vault context για περισσότερη πληροφορία
  --full-permissions    Ενεργοποίηση όλων των tools
  --read-only           Μόνο ανάγνωση (default)

Παράδειγμα:
  python -m src.agent ask "τι είναι το project μας;" --context "Ideas: ..."
""")
        return

    system_prompt = load_instructions()

    if args.context:
        full_prompt = f"Vault Context:\n{args.context}\n\nΕρώτηση: {args.question}"
    else:
        full_prompt = args.question

    full_permissions = args.full_permissions and not args.read_only

    result = call_llm(full_prompt, system_prompt, full_permissions)
    print(result)


if __name__ == "__main__":
    main()
