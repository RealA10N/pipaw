import typing
from random import choice
from dataclasses import dataclass

__all__ = [
    'AppVersion',
    'UserDevice',
    'InstagramUserAgent',
]


@dataclass(frozen=True)
class AppVersion:
    """ The app version is constructed from 5 different numbers, and a string
    that indicates the app (by default, the app name is `Instagram`). Here are
    a couple of version strings for example:

    -   Instagram 195.0.0.31.123
    -   Instagram 196.0.0.0.54
    -   Instagram 76.0.0.15.395
    """

    version: typing.Tuple[int, int, int, int, int]
    """ A tuple representing the version and containing 5 different
    integers. """

    name: str = 'Instagram'
    """ The app name, `Instagram` by default. """

    @property
    def version_str(self,) -> str:
        """ A string that represents the app version only (without the app
        name). Version integers are seperated with dots. """

        return '.'.join(str(i) for i in self.version)

    def __str__(self,) -> str:
        """ A string representation of the app version.
        This string representation is used as a part of the *user agent*. """

        return f'{self.name} {self.version_str}'


@dataclass(frozen=True)
class PhoneResolution:
    """ A simple dataclass that stores the resolution of a phone screen. """

    width: int
    height: int

    def __str__(self,) -> str:
        """ A string representation of the resolution. """
        return f'{self.width}x{self.height}'


@dataclass(frozen=True)
class UserDevice:
    """ A dataclass that contains information about a device, and it's main
    purpose is to generate a *user-agent* string that will be acceptable by
    the Instagram private API. """

    os: str
    os_version: int
    os_release: int
    dpi: int
    resolution: PhoneResolution
    brand: str
    device: str
    model: str
    chipset: str
    version_code: int
    language: str = 'en_US'

    @property
    def details(self,) -> str:
        """ A string that contains additional information about the device.
        The info is provided as a list of values, seperated by ';'. """

        parts = (
            f'{self.os_version}/{self.os_release}',
            f'{self.dpi}dpi',
            self.resolution,
            self.brand,
            self.device,
            self.model,
            self.chipset,
            self.language,
            self.version_code,
        )

        return '; '.join(str(p) for p in parts)

    def __str__(self,) -> str:
        """ Generates and returns a *user-agent* string that represents the
        current device. A couple examples of valid user-agent string are:

        -   Android (29/10; 420dpi; 1080x2181; samsung; SM-N960W; crownqltecs;
            qcom; en_US; 302733750)
        -   Android (24/7.0; 640dpi; 1440x2560; samsung; SM-G930F; herolte;
            samsungexynos8890; en_US; 138226743)
        """

        return f"{self.os!s} ({self.details})"


""" A list of valid Instagram app versions, as `AppVersion` instances. App
version list retrived from https://www.apk4fun.com/history/869/ """
VERSIONS = (
    AppVersion((195, 0, 0, 31, 123)),   # July 2021 👇
    AppVersion((194, 0, 0, 36, 172)),   # June 2021 👇
    AppVersion((193, 0, 0, 45, 120)),
    AppVersion((192, 0, 0, 35, 123)),
    AppVersion((191, 1, 0, 41, 124)),
    AppVersion((190, 0, 0, 36, 119)),
    AppVersion((189, 0, 0, 41, 121)),   # May 2021 👇
    AppVersion((188, 0, 0, 35, 124)),
    AppVersion((187, 0, 0, 32, 120)),
    AppVersion((186, 0, 0, 36, 128)),
    AppVersion((185, 0, 0, 38, 116)),   # April 2021 👇
    AppVersion((183, 0, 0, 40, 116)),
    AppVersion((182, 0, 0, 29, 124)),
    AppVersion((181, 0, 0, 33, 117)),   # March 2021 👇
    AppVersion((180, 0, 0, 31, 119)),
    AppVersion((179, 0, 0, 31, 132)),
    AppVersion((178, 1, 0, 37, 123)),
    AppVersion((177, 0, 0, 30, 119)),
)

DEVICES = (
    UserDevice(
        # Samsung Galaxy Note S9 - August 2018
        brand='samsung',
        device='SM-N960W',
        os='Android',
        os_version=29,
        os_release=10,
        dpi=420,
        resolution=PhoneResolution(1080, 2118),
        model='crownqltecs',
        chipset='qcom',
        version_code=302733750,
    ),
    UserDevice(
        # Samsung Galaxy S8+ - April 2017
        # https://developers.whatismybrowser.com/useragents/parse/47317249instagram-android-sm-g955u-webkit
        brand='samsung',
        device='SM-G955U',
        os='Android',
        os_version=28,
        os_release=9,
        dpi=420,
        resolution=PhoneResolution(1080, 2094),
        model='dream2qltesq',
        chipset='qcom',
        version_code=236572377,
    ),
    UserDevice(
        # Samsung Galaxy A10e - June 2019
        # https://developers.whatismybrowser.com/useragents/parse/50001905instagram-android-sm-a102u-webkit
        brand='samsung',
        device='SM-A102U',
        os='Android',
        os_version=28,
        os_release=9,
        dpi=320,
        resolution=PhoneResolution(720, 1468),
        model='a10e',
        chipset='exynos7885',
        version_code=239490550,
    ),
    UserDevice(
        # Samsung Galaxy S9 - March 2018
        # https://developers.whatismybrowser.com/useragents/parse/49856852instagram-android-sm-g960u-webkit
        brand='samsung',
        device='SM-G960U',
        os='Android',
        os_version=28,
        os_release=9,
        dpi=480,
        resolution=PhoneResolution(1080, 2076),
        model='starqltesq',
        chipset='qcom',
        version_code=240726484,
    ),
    UserDevice(
        # Samsung Galaxy Note10+ - August 2019
        # https://developers.whatismybrowser.com/useragents/parse/50535487instagram-android-sm-n975u-webkit
        brand='samsung',
        device='SM-N975U',
        os='Android',
        os_version=29,
        os_release=10,
        dpi=480,
        resolution=PhoneResolution(1080, 2051),
        model='d2q',
        chipset='qcom',
        version_code=206670927,
    ),
    UserDevice(
        # Motorola One - August 2018
        # https://developers.whatismybrowser.com/useragents/parse/1221393instagram-android-webkit
        brand='motorola',
        device='motorola one',
        os='Android',
        os_version=27,
        os_release=8,
        dpi=320,
        resolution=PhoneResolution(720, 1362),
        model='deen_sprout',
        chipset='qcom',
        version_code=132081645,
    ),
    UserDevice(
        # Samsung Galaxy J7 Prime - September 2016
        # https://developers.whatismybrowser.com/useragents/parse/1218090instagram-android-sm-g610m-webkit
        brand='samsung',
        device='SM-G610M',
        os='Android',
        os_version=23,
        os_release=6,
        dpi=480,
        resolution=PhoneResolution(1080, 1920),
        model='on7xelte',
        chipset='samsungexynos7870',
        version_code=103516666,
    ),
    UserDevice(
        # Samsung Galaxy S10 - February 2019
        # https://developers.whatismybrowser.com/useragents/parse/60168765instagram-android-sm-g973f-webkit
        brand='samsung',
        device='SM-G973F',
        os='Android',
        os_version=29,
        os_release=10,
        dpi=420,
        resolution=PhoneResolution(1080, 2042),
        model='beyond1',
        chipset='exynos9820',
        version_code=256099204,
    ),
)


@dataclass
class InstagramUserAgent:
    """ A dataclass for generating random Instagram valid *user-agent* strings
    and storing them. """

    app: AppVersion
    device: UserDevice

    def __str__(self,) -> str:
        """ Generates a valid Instagram *user-agent* and returns it as a
        string. """

        return f'{self.app!s} {self.device!s}'

    @staticmethod
    def random() -> 'InstagramUserAgent':
        """ Generates and returns a random `InstagramUserAgent` instance. """

        return InstagramUserAgent(
            app=choice(VERSIONS),
            device=choice(DEVICES),
        )
