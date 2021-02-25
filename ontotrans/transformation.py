from abc import ABC, abstractmethod
from tasks import command


class CommandlineStrategy(ABC):
    """
    """
    @abstractmethod
    def write(self, applicationName: str):
        pass


class writeStrategy(CommandlineStrategy):  # write to file
    def write(self, applicationName: str, data: str):
        command.delay(data)


class TransformationContext():
    def __init__(self, applicationName: str, applicationType: str) -> None:
        self._applicationName = applicationName
        self._applicationType = applicationType
        self._cmdlstrategy = writeStrategy()

    @property
    def strategy(self) -> CommandlineStrategy:
        return self._cmdlstrategy

    @strategy.setter
    def strategy(self, strategy: CommandlineStrategy) -> None:
        self._cmdlstrategy = strategy

    def write(self, data) -> None:
        return self._cmdlstrategy.write(self._applicationName, data)
