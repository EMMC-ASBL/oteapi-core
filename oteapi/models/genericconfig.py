"""Generic data model for configuration attributes."""
from typing import Any

from pydantic import BaseModel


class GenericConfig(BaseModel):
    """Generic class for configuration objects.

    The goal of this class is that objects of the class can be treated
    both like a BaseModel and like a dictionary, e.g. subscripted.
    """

    def __init__(self, **kwargs) -> None:
        """Initializer from dictionary."""
        super().__init__(**kwargs)
        for key, value in kwargs.items():
            # Attributes have been set by the call to super() above
            if not self.__contains__(key):
                self.__dict__[key] = value

    def __call__(self, *args, **kwargs) -> Any:
        """Enable calling the function in args[0]."""
        func = args[0]
        if func in dir(self):
            # This object has this function
            found = getattr(self, func)
        elif func in dir(dict):
            # The dictionary representation has the function
            found = getattr(dict(self), func)
        else:
            raise AttributeError(func)
        return found(*args[1:], **kwargs)

    def __contains__(self, name: Any) -> bool:
        """Enable using the 'in' operator on this object."""
        return self.__dict__.__contains__(name)

    def __delitem__(self, key: str) -> None:
        """Enable deletion access through subscription."""
        if key in dir(self):
            self.__delattr__(key)
        else:
            raise KeyError(key)

    def __getitem__(self, key: str) -> Any:
        """Enable read access through subscription."""
        if key in dir(self):
            return getattr(self, key)
        raise KeyError(key)

    def __setitem__(self, key: str, value: Any) -> None:
        """Enable write access through subscription."""
        if key in self.__dict__:
            target_type = type(self.__dict__[key])
            if not value.isinstance(target_type):
                raise TypeError(
                    "Mapped value must be subclass of " + target_type.__name__
                )
        self.__dict__[key] = value
