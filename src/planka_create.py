#!/usr/bin/env python3
"""CLI tool for OpenCode to create Planka cards.

Usage:
  python src/planka_create.py --list-labels
  python src/planka_create.py --title "Τίτλος" --description "..." --labels "l1,l2" --assignee "AP"
"""
import argparse
import asyncio
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).parent.parent / ".env")
sys.path.insert(0, str(Path(__file__).parent))

from planka_client import PlankaClient

_TEAM_MEMBERS = {
    "AP": "Angelos P",
    "AF": "Antonis Frs",
    "ML": "Marios L",
    "NT": "Nikos Tsaata",
    "angelos": "Angelos P",
    "antonis": "Antonis Frs",
    "marios": "Marios L",
    "nikos": "Nikos Tsaata",
}


async def main() -> None:
    p = argparse.ArgumentParser(description="Create a Planka card from the CLI.")
    p.add_argument("--title", default="", help="Card title (max 80 chars)")
    p.add_argument("--description", default="", help="Card description")
    p.add_argument("--labels", default="", help="Comma-separated label names")
    p.add_argument("--assignee", default="", help="Member name or abbreviation (AP/AF/ML/NT)")
    p.add_argument("--list-labels", action="store_true", help="Print available labels and exit")
    args = p.parse_args()

    client = PlankaClient(
        base_url=os.getenv("PLANKA_URL", ""),
        board_id=os.getenv("PLANKA_BOARD_ID", ""),
        email=os.getenv("PLANKA_EMAIL", ""),
        password=os.getenv("PLANKA_PASSWORD", ""),
        list_name=os.getenv("PLANKA_LIST_NAME", "Test Card"),
    )

    if not await client.initialize():
        print("ERROR: Cannot connect to Planka", file=sys.stderr)
        sys.exit(1)

    if args.list_labels:
        print("Διαθέσιμα labels: " + ", ".join(client.get_label_names()))
        await client.close()
        return

    if not args.title:
        print("ERROR: --title is required when not using --list-labels", file=sys.stderr)
        sys.exit(1)

    labels = [l.strip() for l in args.labels.split(",") if l.strip()]
    assignee = args.assignee.strip() or None
    if assignee:
        assignee = _TEAM_MEMBERS.get(assignee, _TEAM_MEMBERS.get(assignee.lower(), assignee))

    card = await client.create_card(
        args.title[:80], args.description, labels, assignee_name=assignee
    )
    await client.close()

    if card:
        print(f"OK: Κάρτα '{card.get('name')}' δημιουργήθηκε (id={card.get('id')})")
    else:
        print("ERROR: Card creation failed", file=sys.stderr)
        sys.exit(1)


asyncio.run(main())
