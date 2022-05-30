from django.core.cache import cache
from functools import wraps


def use_cache(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if len(args) < 2:
            raise ValueError('Invalid Argument for Decorator')

        if len(args) == 2:
            key = f'{args[0].lang}_{args[1]}'
        else:
            key = f'{args[0].lang}_{args[1]}_{args[2]}'
        cached = cache.get(key)
        if not cached:
            return fn(*args, **kwargs)
        return cached
    return wrapper

