import os
import re

with open(os.path.join(os.path.dirname(__file__), 'uri.regexp')) as f:
	pattern = f.read()

URI_REGEX = re.compile(pattern, flags=re.VERBOSE)
