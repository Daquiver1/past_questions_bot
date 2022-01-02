# TODO: INCLUDE THE FILES IN THE NEXT PAGES (later though)
# TODO: ADD AN ALL PAST QUESTIONS FEATURE(later though)

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import requests
import time, re, os

# PATH = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot\\past_questions"
PROFILE = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],}
# 	               "download.default_directory": PATH, "download.extensions_to_open": ""}	# Open externally not with chrome's pdf viewer
URL = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.headless = True	
options.add_experimental_option('prefs', PROFILE)
driver = webdriver.Chrome(service=s, options = options)
# with open("cred\\credentials.txt", "r") as cred: # Retrieve credentials
# 	user_name = cred.readline()
# 	password = cred.readline()
user_name = "10829272"
password = "greenarrow14"

# driver.get(URL)
# login = driver.find_element(By.NAME, "memberID")
# pwd = driver.find_element(By.NAME, "memberPassWord")
# pwd.send_keys(password)
# login.send_keys(user_name) 			# The newline is interpreted as enter
# print("We have began")

# def newest(path):
#     files = os.listdir(path)
#     paths = [os.path.join(path, basename) for basename in files]
    
#     return max(paths, key=os.path.getctime)

# def search_for_pasco(cleaned_pasco_name):
# 	"""
# 	A function to search for past question.
# 	It takes in the concatenated course name and course code.

# 	"""

# 	search = driver.find_element(By.NAME, "keywords")
# 	search_b = driver.find_element(By.NAME, "search")
# 	search.send_keys(f'"{cleaned_pasco_name}"') 		# Double Quotes give accurate queries
# 	search_b.click()

# def display_pascos():
# 	""" 
# 	A function to retrieve the names, year and semester of 
# 	past questions displayed.

# 	inputs: A website address.
# 	output: A print out of the name, year and semester of
# 			past question.
# 	"""
# 	page = requests.get(driver.current_url)

# 	soup = BeautifulSoup(page.content, 'lxml')
# 	pasco = soup.find_all("div", class_="item biblioRecord")
# 	temp = []

# 	for i in pasco:
# 	    pasco1 = i.find("a", class_ = "titleField")
# 	    year1 = i.find("div", class_ = "customField isbnField")
# 	    sem1 = i.find("div", class_ = "customField collationField")
# 	    temp.append(pasco1.get_text() + "\n" + year1.get_text() + "\n" + sem1.get_text())

# 	print("These are the past questions available")
# 	return temp

# def link_of_pasco():
# 	"""
# 	A function to retrieve the links of all the past questions displayed.

# 	inputs: The website address.
# 	output: A dictionary containing the index and the past question link.
# 	"""
# 	page = requests.get(driver.current_url)

# 	soup = BeautifulSoup(page.content, "lxml")
# 	pasco1 = soup.find_all("a", class_ = "titleField")
# 	links = {}
# 	for i in range(1, len(pasco1) + 1): 	# Starts from 1 not 0, 
# 	    links[i] = "https://balme.ug.edu.gh" + pasco1[i-1]["href"]

# 	return links


# def download_pasco(links, choice):
# 	"""
# 	A function to download past questions.
# 	It takes in the link of the past questions available.
# 	User selects a past question.
# 	Downloads the past question.

# 	Input: Dictionary type.
# 	Output: A pdf?
# 	"""

# 	for i, v in links.items():
# 		if int(choice) == i:
# 			driver.get(v)					 # Move to the url of the selected option

# 	file = driver.find_element(By.CLASS_NAME, "openPopUp")
# 	driver.execute_script("arguments[0].click();", file) 
# 	wait = WebDriverWait(driver, 10)
# 	wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
# 	wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()
# 	driver.back()
# 	print("Downloading file, wait a min")
# 	file = newest(PATH)
# 	time.sleep(5)
# 	return file



# if __name__ == '__main__':
# 	name = input("Please enter the course name : ")
# 	search_for_pasco(name)
# 	yaw = display_pascos()
# 	nii = link_of_pasco()
# 	boat = input("Number please: ")
# 	download_pasco(nii, boat)
# 	print(len(yaw))
# 	#links = link_of_pasco()
# 	#download_pasco(links)
# 	#driver.quit()

