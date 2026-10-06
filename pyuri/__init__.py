"""Python URI Handling"""

import sys

if sys.version_info >= (3, 8):
    from importlib.metadata import PackageNotFoundError, version
else:
    # Preserve the version lookup used by the project's Python 2.7/3.6 builds.
    from pkg_resources import DistributionNotFound as PackageNotFoundError
    from pkg_resources import get_distribution

    def version(name):
        return get_distribution(name).version

from .uri import URI

__all__ = ['URI']

try:
    __version__ = version(__name__)
except PackageNotFoundError:
    __version__ = '0.0.0-dev'
