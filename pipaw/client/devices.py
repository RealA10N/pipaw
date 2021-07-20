import typing
from dataclasses import dataclass


@dataclass(frozen=True)
class AppVersion:
    """ The app version is constructed from 5 different numbers, and a string
    that indicates the app (by default, the app name is `Instagram`). Here are
    a couple of version strings for example:

    -   Instagram 195.0.0.31.123 Android
    -   Instagram 196.0.0.0.54 Android
    -   Instagram 76.0.0.15.395 Android
    """

    version: typing.Tuple[int, int, int, int, int]
    """ A tuple representing the version and containing 5 different
    integers. """

    os: str = 'Android'
    """ The os name, `Android` by default. """

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

        return f'{self.name} {self.version_str} {self.os}'


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

    app: AppVersion
    android_version: int
    android_release: int
    dpi: int
    resolution: PhoneResolution
    brand: str
    device: str
    model: str
    chipset: str
    version_code: int
    language: str = 'en_US'

    def __str__(self,) -> str:
        """ Generates and returns a *user-agent* string that represents the
        current device. A couple examples of valid user-agent string are:

        -   Instagram 195.0.0.31.123 Android (29/10; 420dpi; 1080x2181; samsung;
            SM-N960W; crownqltecs; qcom; en_US; 302733750)
        -   Instagram 76.0.0.15.395 Android (24/7.0; 640dpi; 1440x2560; samsung;
            SM-G930F; herolte; samsungexynos8890; en_US; 138226743)
        """

        parts = (
            f'{self.android_version}/{self.android_release}',
            f'{self.dpi}dpi',
            self.resolution,
            self.brand,
            self.device,
            self.model,
            self.chipset,
            self.language,
            self.version_code,
        )

        return f"{self.app!s} ({'; '.join(str(p) for p in parts)})"


DEVICES = (
    UserDevice(
        # Samsung Note S9 - August 2018
        app=AppVersion((195, 0, 0, 31, 123)),
        android_version=29,
        android_release=10,
        dpi=420,
        resolution=PhoneResolution(1080, 2118),
        brand='samsung',
        device='SM-N960W',
        model='crownqltecs',
        chipset='qcom',
        language='en_US',
        version_code=302733750,
    ),
)
