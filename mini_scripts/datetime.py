import datetime
import typing as ty

try:
    import pytz
except ImportError:
    pass

T = ty.TypeVar('T')


def do_datetime(name: str):
    """
    @do_datetime('date')
    class AnyObject:
        date: datetime.datetime

        def __init__(self):
            self.date = datetime.datetime.now()

    any_obj = AnyObject()
    any_obj.date_timestamp
    any_obj.date_native
    any_obj.date_utc
    any_obj.date_moscow
    """

    def to_timestamp(self: T) -> ty.Optional[float]:
        return getattr(self, name).timestamp() or None

    def to_native(self: T) -> ty.Optional[datetime.datetime]:
        _ts = to_timestamp(self)
        if not _ts:
            return None
        return datetime.datetime.fromtimestamp(
            _ts,
            None
        )

    def to_utc(self: T) -> ty.Optional[datetime.datetime]:
        _ts = to_timestamp(self)
        if not _ts:
            return None
        return datetime.datetime.fromtimestamp(
            _ts,
            pytz.utc
        )

    def to_moscow(self: T) -> ty.Optional[datetime.datetime]:
        _ts = to_timestamp(self)
        if not _ts:
            return None
        return datetime.datetime.fromtimestamp(
            _ts,
            pytz.timezone('Europe/Moscow')
        )

    def wrapper(cls: ty.Type[T]) -> ty.Type[T]:
        setattr(cls, name + "_timestamp", property(to_timestamp))
        setattr(cls, name + "_native", property(to_native))
        setattr(cls, name + "_utc", property(to_utc))
        setattr(cls, name + "_moscow", property(to_moscow))
        return cls

    return wrapper
