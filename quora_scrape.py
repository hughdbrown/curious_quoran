
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import requests


def quora_crawl(first_name, last_name, user_email, user_password):
	'''
	INPUT: first and last name, user email and password for Quora account.

	Uses the selenium webdriver to opens Chrome and navigates to user's profile page to scrape the content.
	'''

	# Construct the URL of a user's profile page using their name
	url = 'http://www.quora.com/'+first_name+'-'+last_name
	driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")

	driver.get(url) # Navigate to the desired URL

	# Find the username login form on the Quora login page
	form = driver.find_element_by_class_name('regular_login')
	username = form.find_element_by_name('email')
	username.send_keys(user_email)
	
	# Look for the password field in the Quora 
	password = form.find_element_by_name('password')
	password.send_keys(user_password)
	password.send_keys(Keys.RETURN)

	# Get page source for profile page
	html = driver.page_source
	#print "This is the source for the Quora profile page: \n", html

	soup = BeautifulSoup(html, 'html.parser')

	doc_list = [link.get('href') for link in soup.find_all('a') if link.get('href')!='#']
	
	#print doc_list[11]
	# for tag in soup.find_all('timestamp'):
	# 	print tag.text
   	
 #   	for link in soup.find_all('a'):
 #   		print link.get('href',None),link.get_text()

if __name__ == "__main__":
	first_name = 'Asna'
	last_name = 'Ansari'
	user_email = 'asna.ansari@gmail.com'
	user_password = 'asna1005'
	quora_crawl(first_name, last_name, user_email, user_password)