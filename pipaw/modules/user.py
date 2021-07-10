from .base import InstagramModule


class InstagramUser(InstagramModule):
    """ An object that represents a single Instagram user. """

    def _lookup(self,) -> None:
        'Retrive data about the user using the api. '
        self._data = self._api.user_info(self.pk).get('user')

    @property
    def link(self,) -> str:
        'The link to the user profile. '
        return f'https://www.instagram.com/{self.username}/'

    def __str__(self,) -> str:
        return self.username
