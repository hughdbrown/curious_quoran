from __future__ import print_function

import time
import pickle
import os.path

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import simplejson


def credentials():
	filename = os.path.expanduser("~/.quora-credentials.json")
	with open(filename) as f:
		return simplejson.loads(f.read())


def profile_crawl(url):
	'''
	INPUT: Quora profile URL of the form www.quora.com/Your-Name-#
	OUTPUT: dictionary with lists of strings as values (aggregated questions followed & answers upvoted)

	Uses the selenium webdriver to opens Chrome and navigates to user's profile page to scrape the content.
	'''
	
	# Start the webdriver and navigate to desired url
	driver = webdriver.PhantomJS(executable_path=r'/usr/local/bin/phantomjs')
	# driver.set_window_size(1124, 850)
	#driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")
	driver.set_window_size(1124, 850)
	driver.get('https://www.quora.com/')

	# Need ANY login credentials for scraping, using mine for expediency
	c = credentials()
	user_email = c['email']
	user_password = c['password']

	# Find the username login form on the Quora login page
	form = driver.find_element_by_class_name('regular_login')
	username = form.find_element_by_name('email')
	username.send_keys(user_email)
	
	# Look for the password field in the Quora 
	password = form.find_element_by_name('password')
	password.send_keys(user_password)
	password.send_keys(Keys.RETURN)

	driver.get(url)

	# Simulate scrolling to populate the page with infinite scrolling
	scroll_height=0.1
	while scroll_height < 100:
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
		scroll_height+=1
		time.sleep(0.2)

	# Get page source for profile page
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	
	q_list = [link.get_text() for link in soup.find_all("a", attrs={"class": "question_link"})]
	topic_list = [link.get_text() for link in soup.find_all("a", attrs={"class": "topic_name"})]

	# Now navigate to questions page and scrape
	url2 = url+'/questions'
	driver.get(url2)
	scroll_height=0.1
	while scroll_height < 100:
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight/%s);" %scroll_height)
		scroll_height+=2
		time.sleep(0.2)

	# Get page source for profile page after scrolling to reveal all questions
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	# Collect all questions asked
	asked = [link.get_text() for link in soup.find_all("a", attrs={"class": "question_link"})]
	# total =[t.replace("'s",'') for t in total]	
	output = {'text':q_list, 'topics': topic_list, 'asked': asked}
	return output

if __name__ == "__main__":
	q1 =  profile_crawl('http://www.quora.com/Asna-Ansari')
	print("Questions followed / answers upvoted \n", q1['text'])
	print("Topics followed: \n", q1['topics'])
	print("Questions asked \n", q1['asked'])
	with open("data/quora_data.pkl", "wb") as f:
		pickle.dump(q1, f)