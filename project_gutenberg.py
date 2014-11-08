from bs4 import BeautifulSoup
import pandas as pd
import pickle


def parse_catalog(filepath):
	'''
	INPUT: filepath to catalog in XML format
	OUTPUT: list of text objects with titles, tags, and num downloads"

	The Project Gutenberg resource catalog is one large XML file
	available for download here: http://www.gutenberg.org/feeds/catalog.rdf.bz2

	'''
	f = open(filepath).read()
	
	# Read XML catalog into beautiful soup for parsing, get text
	soup = BeautifulSoup(f)
	text = soup.get_text()
	
	# Cleaning up -- remove newline chars, dashes, and whitespace &pg indicates start of next catalog entry
	splits = text.replace('\n', ' ').replace('--',' ').replace('; ','').split('&pg')
	splits_clean = [s.strip() for s in splits]

	return splits_clean


if __name__=="__main__":
	ext = range(1,8)
	book_list = []
	for e in ext:
		output = parse_catalog('/Users/Asna/Desktop/section{0}.xml'.format(e))
		book_list.append(output)
		
	# Dump raw data to be processed by parser class
	pickle.dump(book_list, open("data/book_list.pkl", "wb"))

	
	
