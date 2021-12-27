# TODO: INCLUDE THE FILES IN THE NEXT PAGES (later though)
# TODO: ADD AN ALL PAST QUESTIONS FEATURE(later though)
 
# An error handling for the following
# Network issue(time out)
# updated site, so change

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from names import pasco_displayed, get_link

PATH = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot\\past_questions"
PROFILE = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
	               "download.default_directory": PATH, "download.extensions_to_open": ""}	# Open externally not with chrome's pdf viewer
s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
#options.headless = True	
options.add_experimental_option('prefs', PROFILE)
driver = webdriver.Chrome(service=s, options = options)
print("We have began")


def name_of_pasco(pasco_name):
	"""
	A function to ask user for name of past_question.
	It takes in the course name and course code.
	It returns the the course name and course code concatenated.

	Output: String type.
	"""
	if not pasco_name.isalpha():		 # Think of changing it to regex, due to the space issue(1)
		print("The name must be only letters.( MATH, STAT..etc)")
		name_of_pasco()
	elif len(pasco_name) != 4:			# Legon course names have 4 characters.
		print("It must have 4 characters.")
		name_of_pasco()

	pasco_code = input("Please enter the course code(eg. 212, 134, 201) : ")
	if not pasco_code.isnumeric():
		print("It must be only numbers. (224, 402..etc)")
		name_of_pasco() 

	if len(pasco_code) != 3: 		# Legon course codes have 3 characters.
		print("It must have 3 characters.")
		name_of_pasco()			

	pasco = pasco_name + " " + pasco_code 	# The site's search won't work if it isn't spaced.
	return pasco

def search_for_pasco(pasco_name):
	"""
	A function to search for past question.
	It takes in the concatenated course name and course code.

	"""

	pasco = name_of_pasco(pasco_name)
	with open("credentials.txt", "r") as cred: # Retrieve credentials
		user_name = cred.readline()
		password = cred.readline()

	url = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
	driver.get(url)
	login = driver.find_element(By.NAME, "memberID")
	pwd = driver.find_element(By.NAME, "memberPassWord")
	pwd.send_keys(password)
	login.send_keys(user_name) 			# The newline is interpreted as enter

	search = driver.find_element(By.NAME, "keywords")
	search_b = driver.find_element(By.NAME, "search")
	search.send_keys(f'"{pasco}"') 		# Double Quotes give accurate queries
	search_b.click()

def display_pascos():
	"""
	A function to display the past questions available.
	It retrieves the past questions displayed on the screen.
	It returns the links of the past questions.

	Output: Dictionary type
	"""

	
	print("These are the past questions available")
	pasco_displayed(driver.current_url)		# Display past questions available
	links = get_link(driver.current_url)	# Links of all past questions available
	if len(links) == 0:
		print("Unfortunately there are no past questions available")
		driver.quit()

	return links

def download_pasco(links):
	"""
	A function to download past questions.
	It takes in the link of the past questions available.
	User selects a past question.
	Downloads the past question.

	Input: Dictionary type.
	Output: A pdf?
	"""

	choice = ""
	while not choice.isnumeric():
		choice = input(f"""
		Please type the number of the one you want to download(Should be a number)
		1 for first.
		2 for second 
		and so on.
		""")
	while not (int(choice) in links.keys()):		# Selected choice has to be in the link.
		print("Choose a number available")
		choice = input()

	for i, v in links.items():
		if int(choice) == i:
			driver.get(v)					 # Move to the url of the selected option

	file = driver.find_element(By.CLASS_NAME, "openPopUp")
	driver.execute_script("arguments[0].click();", file) 
	wait = WebDriverWait(driver, 10)
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
	wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()
	print("Downloading file, wait a min")
	time.sleep(5)
	print("Done Downloading")


if __name__ == '__main__':
	name = input("Please enter the course name(eg. DCIT, UGBS, UGRC) : ")
	search_for_pasco(name)
	links = display_pascos()
	download_pasco(links)
	driver.quit()

