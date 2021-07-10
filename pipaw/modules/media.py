import typing

from .. import modules

# if typing.TYPE_CHECKING:
# from .comment import InstagramComment


class InstagramPost(modules.InstagramModule):
    """ An object that represents a single Instagram post.
    Each instagram post can contain up to 10 images or videos, and they can be
    accessed using the `medias` property. """

    def _lookup(self,) -> None:
        self._api.media_info(self.pk)

    @property
    def link(self,) -> str:
        return f'https://www.instagram.com/p/{self.code}/'


class InstagramMedia:
    pass


class InstagramPhoto(InstagramMedia):
    pass


class InstagramVideo(InstagramMedia):
    pass
