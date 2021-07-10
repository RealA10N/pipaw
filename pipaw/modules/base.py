from abc import ABC, abstractmethod

from ..api import Client
from ..exceptions import PKError


class IntagramModule(ABC):

    def __init__(self,
                 api: Client,
                 pk: int = None,
                 initial_data: dict = None,
                 ) -> None:
        self._api = api
        self._data = initial_data or dict(pk=pk)

        if self.pk is None:
            raise PKError('PK not found')

        if self.pk != pk:
            raise PKError("Given PK doesn't match initial data")

    @abstractmethod
    def _lookup(self,) -> None:
        """ A method that calls the api and updates the `self._data` property
        with updated data. """

    def get(self, name: str, default=None):
        try:
            return self.data[name]
        except LookupError:
            self._lookup()
            return self.data.get(name, default)

    def __getattr__(self, name: str):
        return self.get(name)

    def __repr__(self,) -> str:
        cls = self.__class__.__name__
        return f'{cls}(pk={self.pk})'
