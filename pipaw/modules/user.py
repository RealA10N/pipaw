import typing

from .base import InstagramModule
from .media import InstagramPost


class InstagramUser(InstagramModule):
    """ An object that represents a single Instagram user. """

    def _lookup(self,) -> None:
        'Retrive data about the user using the api. '
        self._data = self._api.user_info(self.pk).get('user')

    @property
    def link(self,) -> str:
        'The link to the user profile. '
        return f'https://www.instagram.com/{self.username}/'

    def posts(self,) -> typing.Generator[InstagramPost, None, None]:
        """ Returns a generator that generates `InstagramPost` instances for
        all posts in the current user feed, from newest (first) to oldest
        (last). """

        # Same params for all requests
        params = {
            'rank_token': self._api.generate_uuid(),
        }

        # Make first api request without `max_id` param
        res = self._api.user_feed(self.pk, **params)
        yield from self.__posts_from_feed_data(res)

        # Make request unit the end of the feed
        # Each time, use the `max_id` param from the previous request
        while 'next_max_id' in res:
            params['max_id'] = res['next_max_id']
            res = self._api.user_feed(self.pk, **params)
            yield from self.__posts_from_feed_data(res)

    def __posts_from_feed_data(self, data: dict) -> typing.List[InstagramPost]:
        """ Recives the raw feed response from the api, and wraps the data with
        InstagramPost instances. """

        for item in data.get('items', list()):
            yield InstagramPost(self._api, initial_data=item)

    def __str__(self,) -> str:
        return self.username
