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
	
	# Clean up -- remove newline chars and dashes, &pg indicates start of next catalog entry
	splits = text.replace('\n', ' ').replace('--',' ').split('&pg')
	splits_clean = [s.strip() for s in splits]
	return splits_clean


if __name__=="__main__":
	print parse_catalog('subset.xml')


