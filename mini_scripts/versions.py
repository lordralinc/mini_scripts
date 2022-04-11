

class SemVer:

    def __init__(self, sem_ver: str):
        self.major, self.minor, self.patch = map(lambda x: int(x), sem_ver.split('.'))

    def __eq__(self, other: "SemVer") -> bool:
        return self.major == other.major and self.minor == other.minor and self.patch == other.patch

    def __lt__(self, other: "SemVer") -> bool:
        if self.major < other.major:
            return True
        if self.major == other.major and self.minor < other.minor:
            return True
        return self.major == other.major and self.minor == other.minor and self.patch < other.patch

    def __le__(self, other: "SemVer") -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: "SemVer") -> bool:
        return not self.__lt__(other) and not self.__eq__(other)

    def __ge__(self, other: "SemVer") -> bool:
        return not self.__lt__(other) or self.__eq__(other)
