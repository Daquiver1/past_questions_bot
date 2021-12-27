# TODO: CHANGE THE VARIABLE NAMES

from bs4 import BeautifulSoup
import requests
from urllib.error import HTTPError
 
def pasco_displayed(link):
	""" 
	A function to retrieve the names, year and semester of 
	past questions displayed.

	inputs: A website address.
	output: A print out of the name, year and semester of
			past question.
	"""

	url = link
	try:
		page = requests.get(url)
	except HTTPError:
		raise HTTPError("The server is down. Try again later")


	soup = BeautifulSoup(page.content, 'lxml')
	pasco = soup.find_all("div", class_="item biblioRecord")
	temp = []

	for i in pasco:
	    pasco1 = i.find("a", class_ = "titleField")
	    year1 = i.find("div", class_ = "customField isbnField")
	    sem1 = i.find("div", class_ = "customField collationField")
	    temp.append(pasco1.get_text() + "\n" + year1.get_text() + "\n" + sem1.get_text())

	return temp


def get_link(link):
	"""
	A function to retrieve the links of all the past questions displayed.

	inputs: The website address.
	output: A dictionary containing the index and the past question link.
	"""

	url = link
	try:
		page = requests.get(url)
	except HTTPError:
		raise HTTPError("The server is down, Try again later.")

	soup = BeautifulSoup(page.content, "lxml")
	pasco1 = soup.find_all("a", class_ = "titleField")
	links = {}
	for i in range(1, len(pasco1) + 1): 	# Starts from 1 not 0, 
	    links[i] = "https://balme.ug.edu.gh" + pasco1[i-1]["href"]

	return links

pasco_displayed("https://balme.ug.edu.gh/past.exampapers/index.php?keywords=%22ugbs+104%22&search=search")
