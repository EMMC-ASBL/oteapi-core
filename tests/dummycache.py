from typing import Dict, List
import json


class DummyCache:

    obj = {}

    def __init__(self, o={}):
        self.obj = o

    async def set(self, id, data) -> None:
        if data:
            self.obj[id] = data

    async def get(self, id) -> Dict:
        return json.dumps(self.obj[id])

    async def keys(self, pattern: str) -> List[str]:
        return self.obj.keys()
