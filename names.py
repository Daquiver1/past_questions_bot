from bs4 import BeautifulSoup

url = "https://balme.ug.edu.gh/past.exampapers/index.php?keywords=%22ugbs+104%22+&search=search"
soup = BeautifulSoup(url, 'lxml')

