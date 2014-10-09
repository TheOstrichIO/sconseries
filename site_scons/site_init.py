# Copyright 2014 The Ostrich / by Itamar O

"""SCons site init script - automatically imported by SConstruct"""

import os
import re

from SCons.Errors import StopError

from site_config import flavors, ENV_OVERRIDES, ENV_EXTENSIONS

def get_base_env(*args, **kwargs):
    """Initialize and return a base construction environment.

    All args received are passed transparently to SCons Environment init.
    """
    # Initialize new construction environment
    env = Environment(*args, **kwargs)  # pylint: disable=undefined-variable
    # If a flavor is activated in the external environment - use it
    if 'BUILD_FLAVOR' in os.environ:
        active_flavor = os.environ['BUILD_FLAVOR']
        if not active_flavor in flavors():
            raise StopError('%s (from env) is not a known flavor.' %
                            (active_flavor))
        print ('scons: Using active flavor "%s" from your environment' %
               (active_flavor))
        env.flavors = [active_flavor]
    else:
        # If specific flavor target specified, skip processing other flavors
        # Otherwise, include all known flavors
        env.flavors = (set(flavors()).intersection(COMMAND_LINE_TARGETS)  # pylint: disable=undefined-variable
                       or flavors())
    # Perform base construction environment customizations from site_config
    if '_common' in ENV_OVERRIDES:
        env.Replace(**ENV_OVERRIDES['_common'])
    if '_common' in ENV_EXTENSIONS:
        env.Append(**ENV_EXTENSIONS['_common'])
    return env

def get_flavored_env(base_env, flavor):
    """Customize and return a flavored construction environment."""
    flavored_env = base_env.Clone()
    # Prepare shared targets dictionary
    flavored_env['targets'] = dict()
    # Allow modules to use `env.get_targets('libname1', 'libname2', ...)` as
    #  a shortcut for adding targets from other modules to sources lists.
    flavored_env.get_targets = lambda *args, **kwargs: \
        get_targets(flavored_env, *args, **kwargs)
    # Apply flavored env overrides and customizations
    if flavor in ENV_OVERRIDES:
        flavored_env.Replace(**ENV_OVERRIDES[flavor])
    if flavor in ENV_EXTENSIONS:
        flavored_env.Append(**ENV_EXTENSIONS[flavor])
    return flavored_env

def process_module(env, module):
    """Delegate build to a module-level SConscript using the specified env.

    @param  env     Construction environment to use
    @param  module  Directory of module

    @raises AssertionError if `module` does not contain SConscript file
    """
    # Verify the SConscript file exists
    sconscript_path = os.path.join(module, 'SConscript')
    assert os.path.isfile(sconscript_path)
    print 'scons: |- Reading module', module, '...'
    # Execute the SConscript file, with variant_dir set to the
    #  module dir under the project flavored build dir.
    targets = env.SConscript(
        sconscript_path,
        variant_dir=os.path.join('$BUILDROOT', module),
        exports={'env': env})
    # Add the targets built by this module to the shared cross-module targets
    #  dictionary, to allow the next modules to refer to these targets easily.
    for target_name in targets:
        # Target key built from module name and target name
        # It is expected to be unique (per flavor)
        target_key = '%s::%s' % (module, target_name)
        assert target_key not in env['targets']
        env['targets'][target_key] = targets[target_name]
        # Add Install-to-binary-directory for Program targets
        for target in targets[target_name]:
            # Program target determined by name of builder
            # Probably a little hacky... (TODO: Improve)
            if target.get_builder().get_name(env) in ('Program',):
                bin_name = '%s.%s' % (module, os.path.basename(str(target)))
                env.InstallAs(os.path.join('$BINDIR', bin_name), target)

def get_targets(env, *args, **kwargs):
    """Return list of target nodes for given target name queries.

    Every positional argument is a singe query.

    Supported query formats:
    1. Fully-Qualified "Module::Target" name queries.
       Matches exact target entries.
    2. Target-name-only queries (no "::" in query).
       Matches all targets with that name, potentially from multiple modules.
       In case of multi-module matches, a warning will be printed.
    3. Wildcard queries (containing "*" in the query).
       Matches all targets whose fully-qualified Module::Target name
       matches the wildcard expression.
       No warning is printed for multiple matches.

    Optionally, pass a keyword argument "no_multi_warn=True" to suppress
    warning messages for unexpected multiple matches for a query.

    Warning messages are always printed when a query results zero matches.
    """
    no_multi_warn = kwargs.pop('no_multi_warn', False)
    def query_to_regex(query):
        """Return RegEx for specified query `query`."""
        # Escape query string
        query = re.escape(query)
        if r'\*' in query:  # '\' because of RE escaping
            # It's a wildcard query
            return re.compile('^%s$' % (query.replace('\\*', '.*'))), False
        if r'\:\:' in query:  # '\' because of RE escaping
            # It's a fully-qualified "Module::Target" query
            return re.compile('^%s$' % (query)), True
        # else - it's a target-name-only query
        return re.compile(r'^[^\:]*\:{2}%s$' % (query)), True
    target_names = set(env['targets'].keys())
    matching_target_names = list()
    for query in args:
        # Remove matched target names to avoid scanning them again
        target_names = target_names.difference(matching_target_names)
        qre, warn = query_to_regex(query)
        match_count = 0
        for target_name in target_names:
            if qre.match(target_name):
                matching_target_names.append(target_name)
                match_count += 1
        # Warn about unexpected scenarios
        if 0 == match_count:
            # No matches for query probably means typo in query
            print ('scons: warning: get_targets query "%s" had no matches' %
                   (query))
        elif warn and (not no_multi_warn) and (1 < match_count):
            # Multiple matches for a "warnable" query might indicate
            #  a too-broad query.
            print ('scons: warning: get_targets query "%s" had %d matches' %
                   (query, match_count))
    # Aggregate all matching target lists and return a single list of targets
    return reduce(lambda acculist, tname: acculist + env['targets'][tname],
                  matching_target_names, [])
