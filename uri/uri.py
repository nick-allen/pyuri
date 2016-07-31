import os
import re

from .validators import *

with open(os.path.join(os.path.dirname(__file__), 'uri.regex')) as f:
	pattern = f.read()

URI_REGEX = re.compile(pattern, flags=re.VERBOSE)


class URI(object):
	"""Data structure abstracting out work needed to parse and build URIs"""

	__modified = False
	__uri = None
	__validators = {}

	def __init__(
		self,
		uri=None,
		scheme=None,
		username=None,
		password=None,
		host=None,
		port=None,
		path=None,
		query=None,
		fragment=None,
		strict=False
	):
		if uri and any([locals()[key] is not None for key in self.__validators]):
			raise ValueError('Cannot provide uri argument alongside any individual parameters')

		self._strict = strict
		self.__validators = {
			'scheme': [StringValidator(self._strict)],
			'username': [StringValidator()],
			'password': [StringValidator()],
			'host': [StringValidator(self._strict)],
			'port': [PortValidator()],
			'path': [StringValidator()],
			'query': [StringValidator()],
			'fragment': [StringValidator()]
		}

		if uri is None:
			self.scheme = scheme
			self.username = username
			self.password = password
			self.host = host
			self.port = port
			self.path = path
			self.query = query
			self.fragment = fragment

		else:
			self.uri = uri

	def __str__(self):
		return self.uri

	def __setattr__(self, key, value):
		if key in self.__validators:
			self.__modified = True

			for validator in self.__validators[key]:
				try:
					value = validator(value)
				except ExitValidation:
					break
				except Exception as error:
					raise ValueError('Unable to set `{}` = `{}`: {}'.format(key, value, error))

		return super(URI, self).__setattr__(key, value)

	@property
	def uri(self):
		"""Cache to prevent recalculating URI unless necessary"""
		if self.__modified:
			self.__uri = self.__parse_uri()

		return self.__uri

	@uri.setter
	def uri(self, value):
		"""Attempt to validate URI and split into individual values"""
		if value == self.__uri:
			return

		match = URI_REGEX.match(value)
		if match is None:
			raise ValueError('Unable to parse URI from `{}`'.format(value))

		for key, value in match.groupdict().items():
			setattr(self, key, value)

	def __parse_uri(self):
		"""Parse complete URI from all values"""
		if self.scheme:
			scheme = '{}://'.format(self.scheme)
		else:
			scheme = ''

		credentials = self.username or ''
		password = self.password or ''

		if credentials and password:
			credentials = '{}:{}'.format(credentials, password)

		if self.port:
			location = '{}:{}'.format(self.host, self.port)
		else:
			location = self.host

		path = self.path or ''
		query = self.query or ''
		fragment = self.fragment or ''

		return scheme + credentials + location + path + query + fragment
