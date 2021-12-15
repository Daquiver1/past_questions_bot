# TODO: MAKE YOUR CODE OOP FORMAT
# TODO: COMMENT YOUR CODE
# TODO: INCLUDE THE FILES IN THE NEXT PAGES
# TODO: ADD ERROR HANDLING
# TODO: MODUALRIZE YOUR CODE, THE BS4 AND SELENIUM
# TODO: TRACK THE EFFICIENCY AND MAKE YOUR CODE MORE EFFICIENT.
# TODO: USE THE UPDATED VERSION OF SELENIUM

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from names import pasco_displayed, get_link

with open("credentials.txt", "r") as cred:
	user_name = cred.readline()
	password = cred.readline()

print(f"""You have 2 options
	- Enter the course code of the subjecct (DCIT 212). Ensure there
	 is a space between the name and the number.
	- Enter the name of the subject (Vectors and Mechanics)""")
name = input()

s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=s)
url = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
driver.get(url)
login = driver.find_element_by_name("memberID")
pwd = driver.find_element_by_name("memberPassWord")
pwd.send_keys(password)
login.send_keys(user_name) # The newline is interpreted as enter

search = driver.find_element_by_name("keywords")
search_b = driver.find_element_by_name("search")
search.send_keys(f'"{name}"') # Double Quotes give accurate queries
search_b.click()
pasco_displayed(driver.current_url)
links = get_link(driver.current_url)
choice = int(input("Please enter which one you want to download: "))

for i, v in links.items():
	if choice == i:
		driver.get(v) # Move to the url of the selected option

file = driver.find_element_by_class_name("openPopUp")
driver.execute_script("arguments[0].click();", file) # read on why the execute works

pdf = driver.find_element_by_id("download")
pdf.click()


time.sleep(50)
#driver.quit()