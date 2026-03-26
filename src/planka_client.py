import asyncio
import logging
import aiohttp

logger = logging.getLogger("OrderlyBot.Planka")


class PlankaClient:
    def __init__(
        self,
        base_url: str,
        board_id: str,
        email: str,
        password: str,
        list_name: str = "Test Card",
    ):
        self._base_url = base_url.rstrip("/")
        self._board_id = board_id
        self._email = email
        self._password = password
        self._list_name = list_name

        self._token: str | None = None
        self._list_id: str | None = None
        self._labels: dict[str, str] = {}  # {name_lower: label_id}
        self._session: aiohttp.ClientSession | None = None
        self._auth_lock = asyncio.Lock()

    # ── Public API ────────────────────────────────────────────────────────────

    async def initialize(self) -> bool:
        """Authenticate and cache board info. Returns True on success."""
        try:
            if not await self._authenticate():
                return False
            if not await self._fetch_board_info():
                return False
            logger.info(
                f"Planka ready. List='{self._list_name}' ({self._list_id}), "
                f"Labels={list(self._labels.keys())}"
            )
            return True
        except Exception as e:
            logger.error(f"Planka initialize error: {e}")
            return False

    async def create_card(
        self, title: str, description: str, label_names: list[str]
    ) -> dict | None:
        """Create a card in the target list and attach labels. Returns card dict or None."""
        if not self._list_id:
            logger.warning("Planka: list_id not set, skipping card creation")
            return None

        data = await self._request(
            "POST",
            f"/api/lists/{self._list_id}/cards",
            json={"name": title[:255], "position": 65535, "description": description},
        )
        if not data:
            return None

        card = data.get("item")
        if not card:
            logger.warning(f"Planka: unexpected card response: {str(data)[:200]}")
            return None

        card_id = card.get("id")
        for name in label_names:
            label_id = self._labels.get(name.lower())
            if label_id and card_id:
                await self._request(
                    "POST",
                    f"/api/cards/{card_id}/labels",
                    json={"labelId": label_id},
                )

        return card

    def get_label_names(self) -> list[str]:
        """Return sorted list of available label names."""
        return sorted(self._labels.keys())

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()

    # ── Internal helpers ──────────────────────────────────────────────────────

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
        return self._session

    async def _authenticate(self) -> bool:
        session = await self._get_session()
        try:
            async with session.post(
                f"{self._base_url}/api/access-tokens",
                json={"emailOrUsername": self._email, "password": self._password},
                timeout=aiohttp.ClientTimeout(total=10),
            ) as r:
                if r.status != 200:
                    logger.error(f"Planka auth failed: HTTP {r.status}")
                    return False
                data = await r.json()
                token = data.get("item")
                if not token or not isinstance(token, str):
                    logger.error(f"Planka auth: unexpected token shape: {str(data)[:100]}")
                    return False
                self._token = token
                return True
        except Exception as e:
            logger.error(f"Planka auth exception: {e}")
            return False

    async def _fetch_board_info(self) -> bool:
        data = await self._request("GET", f"/api/boards/{self._board_id}")
        if not data:
            return False

        included = data.get("included", {})

        # Find target list
        lists = included.get("lists", [])
        for lst in lists:
            if lst.get("name", "").lower() == self._list_name.lower():
                self._list_id = lst["id"]
                break
        if not self._list_id:
            logger.error(
                f"Planka: list '{self._list_name}' not found. "
                f"Available: {[l.get('name') for l in lists]}"
            )
            return False

        # Cache labels
        for label in included.get("labels", []):
            name = label.get("name", "").strip()
            if name:
                self._labels[name.lower()] = label["id"]

        return True

    async def _request(
        self,
        method: str,
        path: str,
        json: dict | None = None,
        retry_on_401: bool = True,
    ) -> dict | None:
        """Central HTTP dispatcher. Returns parsed JSON or None on error."""
        session = await self._get_session()
        headers = {"Authorization": f"Bearer {self._token}"} if self._token else {}
        try:
            async with session.request(
                method,
                f"{self._base_url}{path}",
                json=json,
                headers=headers,
                timeout=aiohttp.ClientTimeout(total=15),
            ) as r:
                if r.status == 401 and retry_on_401:
                    async with self._auth_lock:
                        if not await self._authenticate():
                            return None
                    return await self._request(method, path, json, retry_on_401=False)
                if r.status not in (200, 201):
                    logger.warning(f"Planka {method} {path} → {r.status}")
                    return None
                return await r.json()
        except Exception as e:
            logger.error(f"Planka request error {method} {path}: {e}")
            return None
