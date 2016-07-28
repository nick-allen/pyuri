from nose.tools import assert_equals, assert_is_not_none

from uri.uri import URI_REGEX


valid_uris = [
	('https://google.com/', {
		'scheme': 'https',
		'user': None,
		'pass': None,
		'host': 'google.com',
		'port': None,
		'path': '/',
		'query': None,
		'fragment': None
	})
]


def verify_regex_matches(uri_string, match_dict):
	match = URI_REGEX.match(uri_string)
	assert_is_not_none(match)

	assert_equals(
		match.groupdict(),
		match_dict
	)


def test_uri_regex_matches():
	for uri_string, match_dict in valid_uris:
		yield verify_regex_matches, uri_string, match_dict
