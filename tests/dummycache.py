from typing import Dict, List


class DummyCache:
    async def set(self, id, data) -> None:
        pass

    async def get(self, id) -> Dict:
        return {}

    async def keys(self, pattern: str) -> List[str]:
        return ["1", "2"]
