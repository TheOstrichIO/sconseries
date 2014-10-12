# Copyright 2014 The Ostrich / by Itamar O

"""General build-system utility functions."""

def listify(args):
    """Return args as a list.

    If already a list - returned as is.
    If a single instance of something that isn't a list, return it in a list.
    If "empty" (None or whatever), return a zero-length list ([]).
    """
    if args:
        if isinstance(args, list):
            return args
        return [args]
    return []

def path_to_key(path):
    """Convert path to `key`, by replacing pathseps with periods."""
    return path.replace('/', '.').replace('\\', '.')
