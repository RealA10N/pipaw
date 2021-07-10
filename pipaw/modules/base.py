import typing
from abc import ABC, abstractmethod

from ..exceptions import PKError

if typing.TYPE_CHECKING:
    # Imports that aren't actually used at runtime,
    # and only useful for type checking.
    from ..api import Client


class InstagramBase:
    _api: 'Client'  # The API client object

    def __init__(self, api: 'Client'):
        self._api = api


class InstagramModule(InstagramBase, ABC):
    pk: int  # A unique number used to identify the data across the api.
    _data: dict  # The data, as received form the API.

    def __init__(self,
                 api: 'Client',
                 pk: int = None,
                 initial_data: dict = None,
                 ) -> None:
        super().__init__(api)
        self._data = initial_data or dict(pk=pk)

        if self.pk is None:
            raise PKError('PK not found')

        if pk is not None and self.pk != pk:
            raise PKError("Given PK doesn't match initial data")

    @abstractmethod
    def _lookup(self,) -> None:
        """ A method that calls the api and updates the `self._data` property
        with updated data. """

    def get(self, name: str, default=None):
        try:
            return self._data[name]
        except LookupError:
            self._lookup()
            return self._data.get(name, default)

    def __getattr__(self, name: str):
        return self.get(name)

    def __repr__(self,) -> str:
        cls = self.__class__.__name__
        return f'{cls}(pk={self.pk})'

    def __eq__(self, other) -> bool:
        return self.pk == other

    def __ne__(self, other) -> bool:
        return self.pk != other

    def __hash__(self,) -> int:
        return hash(self.pk)
