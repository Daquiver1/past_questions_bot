# TODO: MAKE YOUR CODE OOP FORMAT
# TODO: COMMENT YOUR CODE
# TODO: INCLUDE THE FILES IN THE NEXT PAGES
# TODO: ADD ERROR HANDLING
# TODO: MODUALRIZE YOUR CODE, THE BS4 AND SELENIUM
# TODO: TRACK THE EFFICIENCY AND MAKE YOUR CODE MORE EFFICIENT.

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
from names import pasco_displayed, get_link
with open("credentials.txt", "r") as cred:
	user_name = cred.readline()
	password = cred.readline()

print(f"""
	Type the course code of the subjecct (eg: DCIT 212). Ensure there
	 is a space between the name and the number.
	""")
name = input()

s = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
path = "C:\\Users\\Anita Agyepong\\Documents\\Daquiver's Quivers\\Python\\past_questions_bot"
profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
               "download.default_directory": path, "download.extensions_to_open": ""}
options.add_experimental_option('prefs', profile)
driver = webdriver.Chrome(service=s, options = options)

url = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
driver.get(url)
login = driver.find_element(By.NAME, "memberID")
pwd = driver.find_element(By.NAME, "memberPassWord")
pwd.send_keys(password)
login.send_keys(user_name) 			# The newline is interpreted as enter

search = driver.find_element(By.NAME, "keywords")
search_b = driver.find_element(By.NAME, "search")
search.send_keys(f'"{name}"') 		# Double Quotes give accurate queries
search_b.click()
pasco_displayed(driver.current_url)		# Display past questions available
links = get_link(driver.current_url)	# Links of all past questions available
print(links)
choice = int(input("Please enter which one you want to download: "))

for i, v in links.items():
	if choice == i:
		driver.get(v) # Move to the url of the selected option

file = driver.find_element(By.CLASS_NAME, "openPopUp")
driver.execute_script("arguments[0].click();", file) # read on why the execute works
wait = WebDriverWait(driver, 10)
wait.until(EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe")))
wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()

time.sleep(20)
#driver.C()