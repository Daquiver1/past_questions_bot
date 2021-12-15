# TODO: CHANGE THE VARIABLE NAMES

from bs4 import BeautifulSoup
import requests

def pasco_displayed(link):
	""" 
	A function to retrieve the names, year and semester of 
	past questions displayed.

	inputs: A website address.
	output: A print out of the name, year and semester of
			past question.
	"""

	url = link
	page = requests.get(url)

	soup = BeautifulSoup(page.content, 'lxml')
	pasco = soup.find_all("div", class_="item biblioRecord")

	for i in pasco:
	    pasco1 = i.find("a", class_ = "titleField")
	    year1 = i.find("div", class_ = "customField isbnField")
	    sem1 = i.find("div", class_ = "customField collationField")
	    print(pasco1.get_text())
	    print(year1.get_text())
	    print(sem1.get_text())
	    print()

def get_link(link):
	""""
	A function to retrieve the links of all the past questions displayed.

	inputs: The website address.
	output: A dictionary containing the index and the past question link.
	"""

	url = link
	page = requests.get(url)

	soup = BeautifulSoup(page.content, "lxml")
	pasco1 = soup.find_all("a", class_ = "titleField")
	links = {}
	for i in range(len(pasco1)):
	    links[i] = "https://balme.ug.edu.gh" + pasco1[i]["href"]

	return links

#get_link("https://balme.ug.edu.gh/past.exampapers/index.php?keywords=%22ugbs+104%22+&search=search")
name = "yaw 1234"
print(name.upper())
