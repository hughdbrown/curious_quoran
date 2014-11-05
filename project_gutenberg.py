# The Project Gutenberg resource catalog is one large XML file (available for download here: http://www.gutenberg.org/feeds/catalog.rdf.bz2).

import re
from bs4 import BeautifulSoup
import pandas as pd


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
	splits = text.replace('\n', ' ').replace('--',' ').replace('; ','').split('&pg')
	splits_clean = [s.strip() for s in splits]
	return splits_clean


if __name__=="__main__":
	ext = range(1,8)
	book_list = []
	for e in ext:
		output = parse_catalog('/Users/Asna/Desktop/section{0}.xml'.format(e))
		# print "Section output: \n", output
		# print '\n'
		# print output[1]
		book_list.append(output)
		print book_list
	
	
