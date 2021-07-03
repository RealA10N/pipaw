import typing
from datetime import timedelta, datetime
from dataclasses import dataclass, field


@dataclass(frozen=True)
class TimedCache:
    value: typing.Any
    delta: timedelta
    created: datetime = field(init=False, default_factory=datetime.now)

    @property
    def expired(self) -> bool:
        """ Returns `True` if the timed cache is no longer up to date. """
        return datetime.now() - self.created > self.delta


class cache:

    @classmethod
    def timed(cls,
              days: float = 0,
              seconds: float = 0,
              microseconds: float = 0,
              milliseconds: float = 0,
              minutes: float = 0,
              hours: float = 0,
              weeks: float = 0,
              ):
        """ A function that returns a decorator. The decorator caches the value
        of the function call for a certion amount of time, as specified with the
        `delta` parameter (using a timedelta instance).

        When using the function, use the keyword-argument `bypass_cache=True`
        to force re-calling the function without loading it from the saved
        cache. """

        delta = timedelta(days=days, seconds=seconds, microseconds=microseconds,
                          milliseconds=milliseconds, minutes=minutes, hours=hours,
                          weeks=weeks)

        def decorator(func: typing.Callable):
            caches: typing.Dict[int, TimedCache] = dict()

            def timed_func(*args, **kwargs):
                key = cls._hash_args(*args, **kwargs)
                bypass = kwargs.pop('bypass_cache', False)

                old_cache = caches.get(key)
                if bypass or not old_cache or old_cache.expired:
                    caches[key] = TimedCache(
                        value=func(*args, **kwargs),
                        delta=delta,
                    )

                return caches[key].value
            return timed_func
        return decorator

    @classmethod
    def forever(cls, func: typing.Callable):
        """ A decorator that caches the function value forever. Stores a collection
        of caches that depend on the arguments and keyword-arguments that are passed
        to the function. """

        caches = typing.Dict[int, typing.Any]

        def cached_func(*args, **kwargs):
            key = cls._hash_args(*args, **kwargs)
            bypass = kwargs.pop('bypass_cache', False)

            if key not in caches or bypass:
                caches[key] = func(*args, **kwargs)
            return caches[key]

        return cached_func

    @staticmethod
    def _hash_args(*args, **kwargs):
        """ Recives a list of arguments and keyword-arguments, and returns a
        hash that represents those arguments. """

        return hash((args, tuple(kwargs.items()),))
