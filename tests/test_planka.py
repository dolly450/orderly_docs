"""Tests for PlankaClient and bot Planka helpers."""
import asyncio
import pytest
import sys
import os
from unittest.mock import AsyncMock, MagicMock, patch, call

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from planka_client import PlankaClient
import bot


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_client(members=None) -> PlankaClient:
    """Return a PlankaClient with pre-populated internal state (no network)."""
    client = PlankaClient(
        base_url="http://planka.test",
        board_id="BOARD1",
        email="test@test.com",
        password="secret",
        list_name="Test Card",
    )
    client._token = "tok"
    client._list_id = "LIST1"
    client._labels = {"feature": "LBL1", "bug": "LBL2"}
    client._members = members if members is not None else {
        "angelos p": "UID_AP",
        "antonis frs": "UID_AF",
        "marios l": "UID_ML",
        "nikos tsaata": "UID_NT",
    }
    return client


# ---------------------------------------------------------------------------
# 1. _resolve_member — name matching
# ---------------------------------------------------------------------------

class TestResolveMember:
    def test_exact_lowercase(self):
        c = make_client()
        assert c._resolve_member("angelos p") == "UID_AP"

    def test_mixed_case(self):
        c = make_client()
        assert c._resolve_member("Angelos P") == "UID_AP"

    def test_first_name_only(self):
        c = make_client()
        # "angelos" should match "angelos p" via first-word comparison
        assert c._resolve_member("angelos") == "UID_AP"

    def test_abbreviation_resolved_via_team_members(self):
        # bot._TEAM_MEMBERS maps "AP" -> "Angelos P" before reaching planka_client
        c = make_client()
        resolved = bot._TEAM_MEMBERS.get("AP")
        assert resolved == "Angelos P"
        assert c._resolve_member(resolved) == "UID_AP"

    def test_unknown_name_returns_none(self):
        c = make_client()
        assert c._resolve_member("Unknown Person") is None

    def test_null_string_returns_none(self):
        c = make_client()
        assert c._resolve_member("null") is None

    def test_empty_string_returns_none(self):
        c = make_client()
        assert c._resolve_member("") is None


# ---------------------------------------------------------------------------
# 2. assign_card — API call
# ---------------------------------------------------------------------------

class TestAssignCard:
    def test_calls_membership_endpoint(self):
        c = make_client()
        c._request = AsyncMock(return_value={"item": {}})

        result = asyncio.run(c.assign_card("CARD1", "Angelos P"))

        assert result is True
        c._request.assert_called_once_with(
            "POST",
            "/api/cards/CARD1/memberships",
            json={"userId": "UID_AP", "role": "editor"},
        )

    def test_returns_false_on_unknown_member(self):
        c = make_client()
        c._request = AsyncMock(return_value=None)

        result = asyncio.run(c.assign_card("CARD1", "Nobody Here"))

        assert result is False
        c._request.assert_not_called()

    def test_returns_false_when_api_fails(self):
        c = make_client()
        c._request = AsyncMock(return_value=None)
        # Force the member to resolve so we can test the API failure path
        c._members["test user"] = "UID_TEST"

        result = asyncio.run(c.assign_card("CARD1", "test user"))

        assert result is False


# ---------------------------------------------------------------------------
# 3. create_card — calls assign_card when assignee provided
# ---------------------------------------------------------------------------

class TestCreateCard:
    def _mock_request(self, card_response=None):
        """Return an AsyncMock that yields a card on POST lists/.../cards and {} otherwise."""
        if card_response is None:
            card_response = {"item": {"id": "CARD99", "name": "Test Card"}}

        async def _req(method, path, json=None, retry_on_401=True):
            if method == "POST" and "/cards" in path and "memberships" not in path and "labels" not in path:
                return card_response
            return {}

        return AsyncMock(side_effect=_req)

    def test_creates_card_no_assignee(self):
        c = make_client()
        c._request = self._mock_request()

        card = asyncio.run(c.create_card("My Title", "desc", []))
        assert card is not None
        assert card["id"] == "CARD99"

    def test_calls_assign_when_assignee_given(self):
        c = make_client()
        c._request = self._mock_request()
        c.assign_card = AsyncMock(return_value=True)

        asyncio.run(c.create_card("Title", "desc", [], assignee_name="Angelos P"))

        c.assign_card.assert_called_once_with("CARD99", "Angelos P")

    def test_no_assign_call_when_no_assignee(self):
        c = make_client()
        c._request = self._mock_request()
        c.assign_card = AsyncMock(return_value=True)

        asyncio.run(c.create_card("Title", "desc", [], assignee_name=None))

        c.assign_card.assert_not_called()

    def test_attaches_labels(self):
        c = make_client()
        posted_paths = []

        async def _req(method, path, json=None, retry_on_401=True):
            posted_paths.append((method, path))
            if method == "POST" and path.endswith("/cards"):
                return {"item": {"id": "CARD99", "name": "T"}}
            return {}

        c._request = AsyncMock(side_effect=_req)
        asyncio.run(c.create_card("T", "d", ["feature", "bug"]))

        label_posts = [p for p in posted_paths if "labels" in p[1]]
        assert len(label_posts) == 2


# ---------------------------------------------------------------------------
# 4. _fetch_members — parses API response correctly
# ---------------------------------------------------------------------------

class TestFetchMembers:
    def test_populates_members_dict(self):
        c = make_client(members={})
        api_response = {
            "items": [
                {"userId": "UID1", "role": "editor"},
                {"userId": "UID2", "role": "viewer"},
            ],
            "included": {
                "users": [
                    {"id": "UID1", "firstName": "Angelos", "lastName": "P", "username": "ap"},
                    {"id": "UID2", "firstName": "Marios", "lastName": "L", "username": "ml"},
                ]
            },
        }
        c._request = AsyncMock(return_value=api_response)

        asyncio.run(c._fetch_members())

        assert c._members == {"angelos p": "UID1", "marios l": "UID2"}

    def test_falls_back_to_username_when_no_name(self):
        c = make_client(members={})
        api_response = {
            "items": [{"userId": "UID3", "role": "editor"}],
            "included": {
                "users": [
                    {"id": "UID3", "firstName": "", "lastName": "", "username": "ntsaata"}
                ]
            },
        }
        c._request = AsyncMock(return_value=api_response)

        asyncio.run(c._fetch_members())

        assert "ntsaata" in c._members

    def test_handles_empty_response_gracefully(self):
        c = make_client(members={})
        c._request = AsyncMock(return_value=None)

        asyncio.run(c._fetch_members())  # should not raise

        assert c._members == {}


# ---------------------------------------------------------------------------
# 5. _build_planka_instruction — Greek language
# ---------------------------------------------------------------------------

class TestBuildPlankaInstruction:
    def test_contains_greek_text(self):
        result = bot._build_planka_instruction('"feature", "bug"')
        # Key Greek words that must appear
        assert "ΟΔΗΓΙΑ" in result
        assert "ΧΡΗΣΤΗ" in result
        assert "block" in result  # English technical term retained

    def test_does_not_contain_english_instruction_header(self):
        result = bot._build_planka_instruction('"feature"')
        assert "SYSTEM NOTE" not in result
        assert "DO NOT SHOW" not in result

    def test_json_schema_preserved(self):
        result = bot._build_planka_instruction('"feature"')
        assert "---PLANKA_CARD---" in result
        assert "---END_CARD---" in result
        assert '"title"' in result
        assert '"description"' in result
        assert '"labels"' in result
        assert '"assignee"' in result


# ---------------------------------------------------------------------------
# 6. _process_planka_block — wires assignee through, no bold injection
# ---------------------------------------------------------------------------

class TestProcessPlankaBlock:
    def _setup_bot(self, planka_client):
        bot._planka_enabled = True
        bot._planka_client = planka_client

    def teardown_method(self, _):
        bot._planka_enabled = False
        bot._planka_client = None

    def test_no_block_returns_unchanged(self):
        self._setup_bot(MagicMock())
        cleaned, msg = asyncio.run(bot._process_planka_block("Hello world"))
        assert cleaned == "Hello world"
        assert msg == ""

    def test_passes_assignee_to_create_card(self):
        mock_client = MagicMock()
        mock_client.create_card = AsyncMock(return_value={"id": "C1", "name": "Fix login"})
        self._setup_bot(mock_client)

        response = (
            "Θα το κάνω.\n"
            "---PLANKA_CARD---\n"
            '{"title": "Fix login", "description": "Details", "labels": [], "assignee": "AP"}\n'
            "---END_CARD---"
        )
        cleaned, msg = asyncio.run(bot._process_planka_block(response))

        mock_client.create_card.assert_called_once()
        _, kwargs = mock_client.create_card.call_args
        # "AP" should have been resolved via _TEAM_MEMBERS to "Angelos P"
        assert kwargs.get("assignee_name") == "Angelos P"

    def test_null_assignee_not_passed(self):
        mock_client = MagicMock()
        mock_client.create_card = AsyncMock(return_value={"id": "C2", "name": "Task"})
        self._setup_bot(mock_client)

        response = (
            "Ok.\n"
            "---PLANKA_CARD---\n"
            '{"title": "Task", "description": "Desc", "labels": [], "assignee": "null"}\n'
            "---END_CARD---"
        )
        asyncio.run(bot._process_planka_block(response))

        _, kwargs = mock_client.create_card.call_args
        assert kwargs.get("assignee_name") is None

    def test_description_not_polluted_with_bold_assignee(self):
        """The old code appended '**Assignee: name**' to description — new code must not."""
        mock_client = MagicMock()
        captured_desc = []

        async def capture_create(title, description, labels, assignee_name=None):
            captured_desc.append(description)
            return {"id": "C3", "name": title}

        mock_client.create_card = capture_create
        self._setup_bot(mock_client)

        response = (
            "Done.\n"
            "---PLANKA_CARD---\n"
            '{"title": "T", "description": "Clean desc", "labels": [], "assignee": "Marios L"}\n'
            "---END_CARD---"
        )
        asyncio.run(bot._process_planka_block(response))

        assert len(captured_desc) == 1
        assert "**Assignee" not in captured_desc[0]
        assert captured_desc[0] == "Clean desc"
