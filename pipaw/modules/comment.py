import typing

from .base import InstagramModule

if typing.TYPE_CHECKING:
    from ..api import Client
    from .media import InstagramPost


class InstagramComment(InstagramModule):

    def __init__(self,
                 api: 'Client',
                 post: 'InstagramPost',
                 pk: int = None,
                 initial_data: dict = None,
                 ) -> None:
        super().__init__(api, pk=pk, initial_data=initial_data)

        self._post = post

    @property
    def post(self,) -> 'InstagramPost':
        'The parent Instagram post in which the comment appears in. '
        return self._post
