import os
import sys
from setuptools import Extension, Distribution
from distutils.errors import *

impa_module = Extension(
    name='impa_core',
    sources=[os.path.dirname(__file__) + '/impa.cpp'],
    extra_compile_args=["-O3","-fPIC", "-Wall", "-std=c++17"],
    include_dirs=['/usr/include/eigen3', '/usr/include/pybind11/',
        os.path.dirname(__file__)],
)

# Create the Distribution instance, using the remaining arguments
# (ie. everything except distclass) to initialize it
dist = Distribution(attrs={
    'script_name': os.path.basename(sys.argv[0]),
    'script_args': ['build_ext', '--inplace'],
    'ext_modules': [impa_module]})

# Find and parse the config file(s): they will override options from
# the setup script, but be overridden by the command line.
dist.parse_config_files()

# Parse the command line and override config files; any
# command-line errors are the end user's fault, so turn them into
# SystemExit to suppress tracebacks.
try:
    ok = dist.parse_command_line()
except DistutilsArgError as msg:
    raise SystemExit("\nerror: %s" % msg)

if ok:
    try:
        dist.run_commands()
    except KeyboardInterrupt:
        raise SystemExit("interrupted")
    except OSError as exc:
        raise SystemExit("error: %s" % (exc,))

    except (DistutilsError,
            CCompilerError) as msg:
        raise SystemExit("error: " + str(msg))

import impa
