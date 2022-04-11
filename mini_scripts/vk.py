
import enum
import random
from collections import namedtuple


class AppType(enum.Enum):
    FIREFOX = enum.auto()
    KATE = enum.auto()
    VK_ME = enum.auto()
    VK_ADMIN = enum.auto()


class HeaderBuilder:
    AndroidVersion = namedtuple('AndroidVersion', ["version", "sdk"])
    ANDROID_VERSIONS = [
        AndroidVersion("Android 11", 30),
        AndroidVersion("Android 10", 29),
        AndroidVersion("Android 9", 28),
        AndroidVersion("Android 8.1", 27),
        AndroidVersion("Android 8", 26),
    ]
    FIREFOX_PATTERN = (
        "Mozilla/5.0 (%(android_version)s; Mobile; rv:68.0) Gecko/68.0 Firefox/94.0"
    )
    KATE_PATTERN = (
        "KateMobileAndroid/80 lite.0-502("
        "%(android_version)s; "
        "SDK %(android_sdk)d; "
        "arm64-v8a; "
        "FBH A%(android_sdk)d; "
        "%(lang)s; "
        "%(resolution_width)dx%(resolution_height)d"
        ")"
    )
    VK_ME_PATTERN = (
        "VKAndroidApp/1.88 7892("
        "%(android_version)s; "
        "SDK %(android_sdk)d; "
        "arm64-v8a; "
        "FBH A%(android_sdk)d; "
        "%(lang)s; "
        "%(resolution_width)dx%(resolution_height)d"
        ")"
    )
    VK_ADMIN_PATTERN = (
        "okhttp/4.0.0-alpha01"
    )

    def __init__(
            self,
            app_type: AppType = AppType.FIREFOX,
            android_version: AndroidVersion = ANDROID_VERSIONS[0],
            extra_lang: str = "ru",
            extra_resolution_width: int = 2340,
            extra_resolution_height: int = 1080
    ):
        self._app_type = app_type
        self._android_version = android_version
        self._extra = {
            "lang": extra_lang,
            "resolution_width": extra_resolution_width,
            "resolution_height": extra_resolution_height
        }

    def set_app_type(self, app_type: AppType = AppType.FIREFOX) -> "HeaderBuilder":
        self._app_type = app_type
        return self

    def set_android_version(self, android_version: AndroidVersion = ANDROID_VERSIONS[0]) -> "HeaderBuilder":
        self._android_version = android_version
        return self

    def random_android_version(self) -> "HeaderBuilder":
        self._android_version = random.choice(self.ANDROID_VERSIONS)
        return self

    def set_extra(self, **extra) -> "HeaderBuilder":
        self._extra = extra
        return self

    def update_extra(self, **extra) -> "HeaderBuilder":
        self._extra.update(extra)
        return self

    def make(self) -> str:
        if self._app_type == AppType.FIREFOX:
            pattern = self.FIREFOX_PATTERN
        elif self._app_type == AppType.KATE:
            pattern = self.KATE_PATTERN
        elif self._app_type == AppType.VK_ME:
            pattern = self.VK_ME_PATTERN
        else:
            pattern = "okhttp/4.0.0-alpha01"
        return pattern % dict(
            android_version=self._android_version.version,
            android_sdk=self._android_version.sdk,
            **self._extra
        )
