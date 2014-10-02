# Copyright 2014 The Ostrich / by Itamar O
# pylint: disable=undefined-variable

"""Flavor-based project main SConstruct script"""

from site_config import modules

# Get the base construction environment
_BASE_ENV = get_base_env()

# Build every selected flavor
for flavor in _BASE_ENV.flavors:
    print 'scons: + Processing flavor', flavor, '...'
    # Prepare flavored environment
    flavored_env = get_flavored_env(_BASE_ENV, flavor)
    # Go over modules to build, and delegate the build to them
    for module in modules():
        process_module(flavored_env, module)
    # Support using the flavor name as a target name for its related targets
    Alias(flavor, flavored_env['BUILDROOT'])
