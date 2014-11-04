
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time


def profile_crawl(first_name, last_name, user_email, user_password):
	'''
	INPUT: first and last name, user email and password for Quora account.
	OUTPUT: list of strings

	Uses the selenium webdriver to opens Chrome and navigates to user's profile page to scrape the content.
	'''

	# Construct the URL of a user's profile page using their name
	url = 'http://www.quora.com/'+first_name+'-'+last_name
	
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

	return q_list

def question_crawl(first_name, last_name, user_email, user_password):
	'''
	INPUT: first and last name, user email and password for Quora account.
	OUTPUT: list of strings (questions asked)

	Uses the selenium webdriver to opens Chrome and navigates to user's questions page.
	'''

	# Construct the URL of a user's profile page using their name
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

	# Collect all question links
	q_asked = [link.get_text() for link in soup.find_all("a", attrs={"class": "question_link"})]
	return q_asked
   	
   	
if __name__ == "__main__":

	# My login info, just a test
	first_name = 'Asna'
	last_name = 'Ansari'
	user_email = 'asna.ansari@gmail.com'
	user_password = 'asna1005'
	print '\n'
	print "Questions followed, answers upvoted: \n" 
	print profile_crawl(first_name, last_name, user_email, user_password)
	print '\n'
	print "Questions asked: \n"
	print question_crawl(first_name, last_name, user_email, user_password)