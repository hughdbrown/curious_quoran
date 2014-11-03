# Hard code in my username and password for expediency -- FIX ME: change this so that it accepts any user's login info

first_name = 'Asna'
last_name = 'Ansari'
user_email = 'asna.ansari@gmail.com'
user_password = 'asna1005'


# Construct the URL of a user's profile page using their name
url = 'http://www.quora.com/'+first_name+'-'+last_name

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(executable_path=r"/Users/Asna/Downloads/chromedriver")

driver.get(url)

# Find the username login form on the Quora login page
form = driver.find_element_by_class_name('regular_login')
username = form.find_element_by_name('email')
username.send_keys(user_email)
#time.sleep(60)

# Look for the password field in the Quora 
password = form.find_element_by_name('password')

password.send_keys(user_password)
password.send_keys(Keys.RETURN)

#time.sleep(60)

# UPDATE does seem to work with user-supplied inputs, albeit very slowly

#driver.close();