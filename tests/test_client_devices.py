from pipaw.client.devices import (
    AppVersion, UserDevice,
    DEVICES, VERSIONS,
)


class TestDefaults:

    def test_existence(self,) -> None:
        """ Asserts that there are default devices and app versions
        provided. """

        assert len(DEVICES) > 0
        assert len(VERSIONS) > 0

    def test_types(self,) -> None:
        """ Asserts that the default decives list actually contains `UserDevice`
        instance, and that the default app versions list actually contains
        `AppVersion` instances. """

        assert all(isinstance(device, UserDevice) for device in DEVICES)
        assert all(isinstance(app, AppVersion) for app in VERSIONS)
