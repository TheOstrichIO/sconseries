# Copyright 2014 The Ostrich / by Itamar O
# pylint: disable=undefined-variable

"""Flavor-based project main SConstruct script with SCons shortcuts"""

from site_config import modules

# Get the base construction environment
_BASE_ENV = get_base_env()

# Build every selected flavor
for flavor in _BASE_ENV.flavors:
    print 'scons: + Processing flavor', flavor, '...'
    flav_bldr = FlavorBuilder(_BASE_ENV, flavor)
    # Go over modules to build, and delegate the build to them
    for module in modules():
        flav_bldr.process_module(module)
