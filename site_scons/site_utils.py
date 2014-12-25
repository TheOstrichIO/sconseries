# Copyright 2014 The Ostrich / by Itamar O

"""General build-system utility functions."""

import os

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

def nop(*args, **kwargs):  # pylint: disable=unused-argument
    """Take arbitrary args and kwargs and do absolutely nothing!"""
    pass

def intersection(*args):
    """Return the intersection of all iterables passed."""
    args = list(args)
    result = set(listify(args.pop(0)))
    while args and result:
        # Finish the loop either when args is consumed, or result is empty
        result.intersection_update(listify(args.pop(0)))
    return result

def module_dirs_generator(max_depth=None, followlinks=False,
                          dir_skip_list=None, file_skip_list=None):
    """Use os.walk to generate directories that contain a SConscript file.

    @param max_depth        Maximal depth for os.walk recursion
                            (None for unlimited)
    @param followlinks      Pass True to make os.walk recurse into dir-links
                            (beware of dreaded symlink loops!)
    @param dir_skip_list    List of callables that take a directory name and
                            return True if the directory should be skipped.
    @param file_skip_list   List of filenames used as dir-skip markers.
                            Directory with marker filename is a "skip dir".
    """
    def should_process(dirpath, filenames):
        """Return True if current directory should be processed.

        Returning False means to skip processing the current directory,
         and every sub-directory thereof.

        @param dirpath          The path to the current directory
        @param filenames        List of filenames in current directory
        """
        for skip_dir_func in listify(dir_skip_list):
            # Skip skip-list directories
            if skip_dir_func(dirpath):
                return False
        if intersection(filenames, file_skip_list):
            # Skip directories with skip-list files
            print 'scons: |- Skipping %s (skip marker found)' % (dirpath)
            return False
        return True
    top = '.'
    for dirpath, dirnames, filenames in os.walk(top, topdown=True,
                                                followlinks=followlinks):
        # Find path relative to top
        rel_path = os.path.relpath(dirpath, top) if (dirpath != top) else ''
        if rel_path:
            if not should_process(rel_path, filenames):
                # prevent os.walk from recursing deeper and skip
                dirnames[:] = []
                continue
            if max_depth:
                # Skip too-deep directories
                max_depth = int(max_depth)
                assert max_depth > 0
                # Calculate current depth relative to top path
                depth = rel_path.count(os.path.sep) + 1
                if depth == max_depth:
                    # prevent os.walk from recursing deeper
                    dirnames[:] = []
                if depth > max_depth:
                    # shouldn't reach here though - shout and skip
                    print 'w00t?! Should not reach here ... o_O'
                    continue
        # Yield directory with SConscript file
        if 'SConscript' in filenames:
            yield rel_path
