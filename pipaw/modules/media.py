import typing
from datetime import datetime

from .. import modules

# if typing.TYPE_CHECKING:
# from .comment import InstagramComment


class InstagramPost(modules.InstagramModule):
    """ An object that represents a single Instagram post.
    Each instagram post can contain up to 10 images or videos, and they can be
    accessed using the `medias` property. """

    code: str               # A unique code that represents the post
    taken_at: int           # Unix timestamp when posted
    comment_count: int      # Number of comments on post
    has_liked: bool         # `True` if the api user has liked the post

    def _lookup(self,) -> None:
        self._data = self._api.media_info(self.pk)

    @property
    def link(self,) -> str:
        return f'https://www.instagram.com/p/{self.code}/'

    @property
    def created(self,) -> datetime:
        """ The exact moment in which the post was uploaded to the Instagram
        servers, as a `datetime` instance. """

        return datetime.fromtimestamp(self._data.get('taken_at'))

    @property
    def user(self,) -> 'modules.InstagramUser':
        """ Returns an `InstagramUser` instance that represents the user that
        uploaded the post. """

        return modules.InstagramUser(
            self._api,
            initial_data=self._data.get('user'),
        )


class InstagramMedia:
    pass


class InstagramPhoto(InstagramMedia):
    pass


class InstagramVideo(InstagramMedia):
    pass