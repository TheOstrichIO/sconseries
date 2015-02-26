# Copyright 2015 The Ostrich / by Itamar O
# pylint: disable=too-few-public-methods

"""External libraries data structures."""

from site_utils import listify

class ExtLib(object):
    """External Library class."""

    def __init__(self, lib_name, libs=None, include_paths=None, lib_paths=None):
        """Initialize external library instance.

        @param lib_name       Symbolic name of library (or library-group)
        @param libs           Identifiers of libraries to link with
                              (if not specified, `lib_name` is used)
        @param include_paths  Additional include search paths
        @param lib_paths      Additional library search paths
        """
        super(ExtLib, self).__init__()
        self.name = lib_name
        self.libs = listify(libs) if libs is not None else [lib_name]
        self.cpp_paths = listify(include_paths)
        self.lib_paths = listify(lib_paths)

    def __repr__(self):
        return u'%s' % (self.name)

class HeaderOnlyExtLib(ExtLib):
    """Header-only external library class.

    Same as ExtLib, supporting only extra include paths.
    This is useful to enforce header-only external libraries
    (like many boost sub-libraries).
    """

    def __init__(self, *args, **kwargs):
        """Initialize header-only external library instance."""
        # Extract keyword-arguments not allowed with header-only libraries
        kwargs.pop('libs')
        kwargs.pop('lib_paths')
        if len(args) >= 3:
            assert 'include_paths' not in kwargs
            kwargs['include_paths'] = args[2]
        super(HeaderOnlyExtLib, self).__init__(args[0], **kwargs)
