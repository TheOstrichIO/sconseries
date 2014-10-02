# Copyright 2014 The Ostrich / by Itamar O
# pylint: disable=bad-whitespace

"""SCons site config script"""

import os

# Directory for build process outputs (object files etc.)
_BUILD_BASE = 'build'

def modules():
    """Generate modules to build.

    Each module is a directory with a SConscript file.
    Modules must be yielded in order of dependence,
     such that modules[i] does not depend on modules[j] for every i<j.
    """
    yield 'AddressBook'
    yield 'Writer'

# Dictionary of flavor-specific settings that should override values
#  from the base environment (using env.Replace).
# `_common` is reserved for settings that apply to the base env.
ENV_OVERRIDES = {
    '_common': dict(
        # Use clang compiler by default
        CC          = 'clang',
        CXX         = 'clang++',
    ),
    'debug': dict(
        BUILDROOT = os.path.join(_BUILD_BASE, 'debug'),
    ),
    'release': dict(
        BUILDROOT = os.path.join(_BUILD_BASE, 'release'),
    ),
}

# Dictionary of flavor-specific settings that should extend values
#  from the base environment (using env.Append).
# `_common` is reserved for settings that apply to the base env.
ENV_EXTENSIONS = {
    '_common': dict(
        # Common flags for all C++ builds
        CCFLAGS = ['-std=c++11', '-Wall', '-fvectorize', '-fslp-vectorize'],
        # Modules should be able to include relative to build root dir
        CPPPATH = ['#$BUILDROOT'],
    ),
    'debug': dict(
        # Extra flags for debug C++ builds
        CCFLAGS = ['-g', '-DDEBUG'],
    ),
    'release': dict(
        # Extra flags for release C++ builds
        CCFLAGS = ['-O2', '-DNDEBUG'],
    ),
}

def flavors():
    """Generate supported flavors.

    Each flavor is a string representing a flavor entry in the
    override / extension dictionaries above.
    Each flavor entry must define atleast "BUILDROOT" variable that
    tells the system what's the build base directory for that flavor.
    """
    # Use the keys from the env override / extension dictionaries
    for flavor in set(ENV_EXTENSIONS.keys() + ENV_OVERRIDES.keys()):
        # Skip "hidden" records
        if not flavor.startswith('_'):
            yield flavor
