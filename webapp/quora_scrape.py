
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import pickle


def profile_crawl(url):
	'''
	INPUT: first and last name, user email and password for Quora account.
	OUTPUT: list of strings

	Uses the selenium webdriver to opens Chrome and navigates to user's profile page to scrape the content.
	'''

	# Construct the URL of a user's profile page using their name
	#url = 'http://www.quora.com/'+first_name+'-'+last_name
	#url = 'http://www.quora.com/William-Lane-2'
	#url = 'http://www.quora.com/Charles-Durand-1'
	#url = 'http://www.quora.com/Tammy-Lee-17'
	url = str(url)
	
	# Start the webdriver and navigate to desired url
	driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")
	driver.get(url)

	# Find the username login form on the Quora login page
	form = driver.find_element_by_class_name('regular_login')
	username = form.find_element_by_name('email')
	username.send_keys(user_email)
	
	# Look for the password field in the Quora 
	password = form.find_element_by_name('password')
	password.send_keys(user_password)
	password.send_keys(Keys.RETURN)


	# Simulate scrolling to populate the page with infinite scrolling
	scroll_height=0.1
	while scroll_height < 100:
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
		scroll_height+=1
		time.sleep(0.5)

	# Get page source for profile page
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	
	q_list = [link.get_text() for link in soup.find_all("a", attrs={"class": "question_link"})]
	#topic_list = [link.get_text() for link in soup.find_all("a", attrs={"class": "topic_name"})]

	#return question list as a string 
	return str(q_list), str(topic_list)

def question_crawl(first_name, last_name, user_email, user_password):
	'''
	INPUT: first and last name, user email and password for Quora account.
	OUTPUT: list of strings (questions asked)

	Uses the selenium webdriver to opens Chrome and navigates to user's questions page.
	'''

	# Construct the URL of a user's questions asked page using their name
	url = 'http://www.quora.com/'+first_name+'-'+last_name+'/questions'
	
	# Start the webdriver and navigate to desired url
	driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")
	driver.get(url)

	# Find the username login form on the Quora login page
	form = driver.find_element_by_class_name('regular_login')
	username = form.find_element_by_name('email')
	username.send_keys(user_email)
	
	# Look for the password field in the Quora 
	password = form.find_element_by_name('password')
	password.send_keys(user_password)
	password.send_keys(Keys.RETURN)


	# Simulate scrolling to populate the page with infinite scrolling
	scroll_height=0.1
	while scroll_height < 100:
		driver.execute_script("window.scrollTo(0,document.body.scrollHeight/%s);" %scroll_height)
		scroll_height+=2
		time.sleep(0.1)

	# Get page source for profile page after scrolling to reveal all questions
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')

	# Collect all question links from the page source
	q_asked = [link.get_text() for link in soup.find_all("a", attrs={"class": "question_link"})]
	return q_asked
   	
   	
if __name__ == "__main__":

	# First and last name of desired user. My name as a test
	first_name = 'Asna'
	last_name = 'Ansari'

	# Need ANY login credentials for scraping, just using mine as example
	user_email = 'asna.ansari@gmail.com'
	user_password = 'asna1005'
	q1 =  profile_crawl(first_name, last_name, user_email, user_password)
	q2 = question_crawl(first_name, last_name, user_email, user_password)
	total = q1+q2
	total =[t.replace("'s",'') for t in total]
	print total

	# Quora dump to be parsed with text parser
	pickle.dump(total, open("data/quora_data.pkl", "wb"))