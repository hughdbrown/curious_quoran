# The Project Gutenberg resource catalog is one large XML file (available for download here: http://www.gutenberg.org/feeds/catalog.rdf.bz2).

import re
from bs4 import BeautifulSoup


def parse_catalog(filepath):
	'''
	INPUT: filepath to catalog in XML format
	OUTPUT: list of text objects with titles, tags, and num downloads"
	'''
	f = open(filepath).read()
	
	# Read XML catalog into beautiful soup for parsing, get text
	soup = BeautifulSoup(f)
	text = soup.get_text()
	
	# Clean up -- remove newline chars, dashes, and whitespace &pg indicates start of next catalog entry
	splits = text.replace('\n', ' ').replace('--',' ').split('&pg')
	splits_clean = [s.strip() for s in splits]
	return splits_clean


if __name__=="__main__":
	output = parse_catalog('subset.xml')
	print "Same parsed book metadata: ", output[1]
	print "\n"
	print "Download count: ", re.findall('[0-9+]\w+',output[1])[-1]


