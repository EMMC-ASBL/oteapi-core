from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urlparse
from uuid import uuid4
import tempfile
import pandas as pd
import requests
import pysftp


class CommandlineStrategy(ABC):
    """
    """
    @abstractmethod
    def read(self, uri: str):
        pass

