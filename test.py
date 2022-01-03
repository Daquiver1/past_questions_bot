from selenium import webdriver
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time, re

# Used when polling. 

# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
#PATH = "path to folder"
#s = Service(ChromeDriverManager().install())
#options = webdriver.ChromeOptions()
#options.headless = True	
#driver = webdriver.Chrome(service=s, options = options)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
PATH = "/tmp"
PROFILE = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
 	               "download.default_directory": PATH, "download.extensions_to_open": ""}	# Open externally not with chrome's pdf viewer
chrome_options.add_experimental_option('prefs', PROFILE)
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
URL = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")

# Log in
driver.get(URL)
login = driver.find_element(By.NAME, "memberID")
pwd = driver.find_element(By.NAME, "memberPassWord")
button = driver.find_element(By.NAME, "logMeIn")
pwd.send_keys(PASSWORD)
login.send_keys(USER_NAME) 			# The newline is interpreted as enter
button.click()
print("Logged in succesfully")

def newest(path):
	"""
	A function to that returns the path of the downloaded file.
	It takes in the downlaod directory path and returns the most recent one.
	"""

	files = os.listdir(path)
	paths = [os.path.join(path, basename) for basename in files if basename.endswith(".pdf")] 

	return max(paths, key=os.path.getctime)
    

def search_for_pasco(cleaned_pasco_name):
	"""
	A function to search for past question.
	It takes in the concatenated course name and course code.

	"""

	search = driver.find_element(By.NAME, "keywords")
	search_b = driver.find_element(By.NAME, "search")
	search.send_keys(f'"{cleaned_pasco_name}"') 		# Double Quotes give accurate queries
	search_b.click()

def display_pascos():
	""" 
	A function to retrieve the names, year and semester of 
	past questions displayed.

	output: A print-out of the name, year and semester of
			past question.
	"""

	page = requests.get(driver.current_url)

	soup = BeautifulSoup(page.content, 'lxml')
	pasco = soup.find_all("div", class_="item biblioRecord")
	temp = []

	for i in pasco:
	    pasco1 = i.find("a", class_ = "titleField")
	    year1 = i.find("div", class_ = "customField isbnField")
	    sem1 = i.find("div", class_ = "customField collationField")
	    temp.append(pasco1.get_text() + "\n" + year1.get_text() + "\n" + sem1.get_text())

	return temp

def link_of_pasco():
	"""
	A function to retrieve the links of all the past questions displayed.

	output: A dictionary containing the index and the past question link.
	"""

	page = requests.get(driver.current_url)

	soup = BeautifulSoup(page.content, "lxml")
	pasco1 = soup.find_all("a", class_ = "titleField")
	links = {}
	for i in range(1, len(pasco1) + 1): 	# Starts from 1 not 0, 
	    links[i] = "https://balme.ug.edu.gh" + pasco1[i-1]["href"]

	return links


def download_pasco(links, choice):
	"""
	A function to download past questions.
	It takes in the links of the past questions and the users choice.
	Returns the path of the downloaded past question. 

	"""

	for i, v in links.items():
		if int(choice) == i:
			driver.get(v)					 # Move to the url of users choice.

	file = driver.find_element(By.CLASS_NAME, "openPopUp")
	driver.execute_script("arguments[0].click();", file)		# screen displayed is a frame, so adapts to a frame.
	wait = WebDriverWait(driver, 10)
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
	wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()
	driver.back()
	time.sleep(2)							# wait for file to be downloaded before moving on.
	file = newest(PATH)
	return file

if __name__ == '__main__':
	name = input("Please enter the course name : ")
	search_for_pasco(name)
	questions = display_pascos()
	pasco_links = link_of_pasco()
	user_choice = input("Number please: ")
	download_pasco(pasco_links, user_choice)

