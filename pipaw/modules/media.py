import typing
from datetime import datetime

from .. import modules


class MediaTypes:
    """ The Instagram API uses numbers to catalog different media types.
    In the API, a photo is represented by the integer `1`, a video by the
    integer `2` and a collection of videos and photos (album / carousel post) 
    by the integer `3`. """

    PHOTO = 1
    VIDEO = 2
    ALBUM = 8


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

    @property
    def medias(self,) -> typing.Tuple['InstagramMedia']:

        if self.media_type == MediaTypes.ALBUM:
            # If the post is a collection of images and videos
            # Returns a tuple with multiple `InstagramMedia` instances.

            return tuple(
                self.__data_to_media(media_data)
                for media_data in self.carousel_media
            )

        else:
            # If not an album, returns a tuple of length 1
            return (self.__data_to_media(self._data), )

    @staticmethod
    def __data_to_media(data: dict,) -> 'InstagramMedia':
        """ Recives a data dictionary, and converts it into an `InstagramPhoto`
        or an `InstagramVideo` instance. """

        if data.get('media_type') == MediaTypes.VIDEO:
            return InstagramVideo(data)

        else:
            # Assuming that the image format is the default.
            # That's a safe thing to assume, because other media types have
            # image information as well (for example, each video has also
            # an image that is used as a thumbnail and is provided by the API).
            return InstagramMedia(data)


class InstagramMedia:
    """ An object that wraps and represents a single piece of media from the
    Instagram servers. One media usually has multiple versions in different sizes
    and qualities, and they are all accessible via the `image_versions` property.

    The `url`, `width`, `height`, and `size` properties will return information
    from the version with the heighest quality. """

    def __init__(self,
                 data: dict,
                 ) -> None:
        self._data = data

    @property
    def url(self,) -> str:
        return self.best_image.url

    @property
    def image_versions(self,) -> typing.Tuple['MediaVersion']:
        """ A tuple containing all avaliable versions of the media, as
        `MediaVersion` objects. """

        return tuple(
            MediaVersion(data)
            for data in self._data['image_versions2']['candidates']
        )

    @property
    def best_image(self,) -> 'MediaVersion':
        """ The media version with the heighest resolution from the avaliable
        media versions. """

        return max(
            self.image_versions,
            key=lambda img: img.pixels,
        )

    @property
    def width(self,) -> int:
        """ The width of the original, not compressed image. """
        return self._data.get('original_width')

    @property
    def height(self,) -> int:
        """ The height of the original, not compressed image. """
        return self._data.get('original_height')

    @property
    def size(self,) -> typing.Tuple[int, int]:
        """ The size of the original, not compressed image. """
        return (self.width, self.height)


class InstagramVideo(InstagramMedia):
    """ An object that represents a video from the Instagram servers. One media
    usually has multiple versions in different sizes and qualities, and they are
    all accessible via the `video_versions` property. 

    The `url`, `width`, `height`, and `size` properties will return information
    from the version with the heighest quality.

    In addition to the video, the Instagram API provides images that act like
    thumbnails and are shown before a user clicks on the video to actually play
    it. Those images are avaliable using the `image_versions` and `best_image`
    properties.

    """

    @property
    def url(self,) -> str:
        return self.best_video.url

    @property
    def video_versions(self,) -> typing.Tuple['MediaVersion']:
        """ A tuple containing all avaliable versions of the media, as
        `MediaVersion` objects. """

        return tuple(
            MediaVersion(data)
            for data
            in self._data.get('video_versions')
        )

    @property
    def best_video(self,) -> 'MediaVersion':
        """ The media version with the heighest resolution from the avaliable
        media versions. """

        return max(
            self.video_versions,
            key=lambda vid: vid.pixels,
        )

    @property
    def audio(self,) -> bool:
        """ `True` if the video has sound. """
        return self._data.get('has_audio')

    @property
    def duration(self,) -> float:
        """ The duration of the video, in seconds. """
        return self._data.get('video_duration')

    @property
    def views(self,) -> int:
        """ The number of views the video has at the moment. """
        return self._data.get('view_count')

    @property
    def plays(self,) -> int:
        """ The number of times the video was played. """
        return self._data.get('play_count')


class MediaVersion:

    def __init__(self, data: dict, ) -> None:
        self._data = data

    @property
    def url(self,) -> str:
        return self._data.get('url')

    @property
    def width(self,) -> int:
        return self._data.get('width')

    @property
    def height(self,) -> int:
        return self._data.get('height')

    @property
    def size(self,) -> typing.Tuple[int, int]:
        """ Returns the image size, as a tuple of length 2. """
        return (self.width, self.height)

    @property
    def pixels(self,) -> int:
        """ The amount of pixels in the image. """
        return self.width * self.height

    def __repr__(self,) -> str:
        cls = self.__class__.__name__
        return f'{cls}(size={self.width}x{self.height})'
