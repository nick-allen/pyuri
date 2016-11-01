"""Python URI Handling"""

from .uri import URI



__all__ = [
	'URI'
]

__version__ = '0.2.0'
VERSION = tuple(map(int, __version__.split('.')))
