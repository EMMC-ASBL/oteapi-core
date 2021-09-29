from abc import ABC, abstractmethod

class Strategy(ABC):
    """
    The Strategy interface declares operations common to all supported versions
    of some algorithm.

    The Context uses this interface to call the algorithm defined by Concrete
    Strategies.
    """
    @abstractmethod
    def __init__(self, prefix):
        self._prefix = prefix


    @abstractmethod
    async def do_something(self):
        """
        something
        """
        pass

    @property
    def prefix(self) -> str:
        """
        Fetch the strategy prefix path
        """
        return self._prefix