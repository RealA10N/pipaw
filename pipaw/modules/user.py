import typing

from .. import modules


class InstagramUser(modules.InstagramModule):
    """ An object that represents a single Instagram user. """

    # Profile information
    username: str
    full_name: str
    category: str
    biography: str
    external_url: str

    # Booleans
    is_private: bool
    is_verified: bool
    is_memorialized: bool
    is_business: bool
    has_anonymous_profile_picture: bool

    # Media
    media_count: int
    follower_count: int
    following_count: int
    total_igtv_videos: int
    total_ar_effects: int

    # TODO: Profile picture wrapper

    def _lookup(self,) -> None:
        'Retrive data about the user using the api. '
        self._data = self._api.user_info(self.pk).get('user')

    @property
    def link(self,) -> str:
        'The link to the user profile. '
        return f'https://www.instagram.com/{self.username}/'

    def posts(self,) -> typing.Generator['modules.InstagramPost', None, None]:
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

    def __posts_from_feed_data(self, data: dict) -> typing.List['modules.InstagramPost']:
        """ Recives the raw feed response from the api, and wraps the data with
        InstagramPost instances. """

        for item in data.get('items', list()):
            yield modules.InstagramPost(self._api, initial_data=item)

    def __str__(self,) -> str:
        return self.username
