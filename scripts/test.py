# TODO: INCLUDE THE FILES IN THE NEXT PAGES (later though)
# TODO: ADD ERROR HANDLING
# TODO: ADD AN ALL PAST QUESTIONS FEATURE(later though)

# Network issue(time out)
# updated site, so change
# Document your functions


from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time, sys
from names import pasco_displayed, get_link
PATH = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot"
PROFILE = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
	               "download.default_directory": PATH, "download.extensions_to_open": ""}
s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
	
options.add_experimental_option('prefs', PROFILE)
driver = webdriver.Chrome(service=s, options = options)

def name_of_pasco():
	pasco_name = input("Please enter the course name(eg. DCIT, UGBS, UGRC) : ")
	if not pasco_name.isalpha(): # Think of changing it to regex, due to the space issue(1)
		print("The name must be only letters.( MATH, STAT..etc)")
		name_of_pasco()
	elif len(pasco_name) != 4:
		print("It must have 4 characters.")
		name_of_pasco()

	pasco_code = input("Please enter the course code(eg. 212, 134, 201) : ")
	if not pasco_code.isnumeric():
		print("It must be only numbers. (224, 402..etc)")
		name_of_pasco() 

	if len(pasco_code) != 3: 	# There might be an error, it's still asking for 3 chars, even when it was 3 chars.
		print("It must have 3 characters.")
		name_of_pasco()			# Read on function calls, recursive how they work with variables.

	pasco = pasco_name + " " + pasco_code
	return pasco

def search_for_pasco():

	pasco = name_of_pasco()
	with open("credentials.txt", "r") as cred:
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

	
	print("These are the past questions available")
	pasco_displayed(driver.current_url)		# Display past questions available
	links = get_link(driver.current_url)	# Links of all past questions available
	if len(links) == 0:
		print("Unfortunately there are no past questions available")
		sys.exit()

	return links

def download_pasco(links):
	choice = ""
	while not choice.isnumeric():
		choice = input(f"""
		Please type the number of the one you want to download(Should be a number)
		1 for first.
		2 for second 
		and so on.
		""")
	while not (int(choice) in links.keys()):
		print("Choose a number available")
		choice = input()

	for i, v in links.items():
		if int(choice) == i:
			driver.get(v) # Move to the url of the selected option

	file = driver.find_element(By.CLASS_NAME, "openPopUp")
	driver.execute_script("arguments[0].click();", file) 
	wait = WebDriverWait(driver, 10)
	wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
	wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()

search_for_pasco()
links = display_pascos()
download_pasco(links)

# #driver.C()