# Copyright 2014 The Ostrich / by Itamar O
# pylint: disable=undefined-variable,star-args,invalid-name

"""Modules-based project main SConstruct script"""

import os

def modules():
    """Generate modules to build.

    Each module is a directory with a SConscript file.
    Modules must be yielded in order of dependence,
     such that modules[i] does not depend on modules[j] for every i<j.
    """
    yield 'AddressBook'
    yield 'Writer'

# Directory for build process outputs (object files etc.)
build_dir = 'build'

env = Environment()
# Allow including from project build base dir
env.Append(CPPPATH=['#%s' % (build_dir)])
# Prepare shared targets dictionary
env['targets'] = dict()
# Allow modules to use `env.get_targets('libname1', 'libname2', ...)` as
#  a shortcut for adding targets from other modules to sources lists.
env.get_targets = lambda *args, **kwargs: get_targets(env, *args, **kwargs)

# Go over modules to build, and include their SConscript files
for module in modules():
    # Verify the SConscript file exists
    sconscript_path = os.path.join(module, 'SConscript')
    assert os.path.isfile(sconscript_path)
    print 'scons: |- Reading module', module, '...'
    # Execute the SConscript file, with variant_dir set to the
    #  module dir under the project build dir.
    targets = env.SConscript(sconscript_path,
                             variant_dir=os.path.join(build_dir, module),
                             exports={'env': env})
    # Add the targets built by this module to the shared cross-module targets
    #  dictionary, to allow the next modules to refer to these targets easily.
    for target_name in targets:
        # Target key built from module name and target name
        # It is expected to be unique
        target_key = '%s::%s' % (module, target_name)
        assert target_key not in env['targets']
        env['targets'][target_key] = targets[target_name]
