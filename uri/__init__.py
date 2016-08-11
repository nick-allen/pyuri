"""Python URI Handling"""

from .uri import URI



__all__ = [
	'URI'
]

__version__ = '0.1.1'
VERSION = tuple(map(int, __version__.split('.')))
