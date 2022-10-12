import logging
import os
import sys
import time
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup
from selenium import webdriver

# Polling Selenium setup
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Used when polling.
# from webdriver_manager.chrome import ChromeDriverManager
# PATH = "path to folder"
# s = Service(ChromeDriverManager().install())
# options = webdriver.ChromeOptions()
# options.headless = True
# driver = webdriver.Chrome(service=s, options = options)
# Constants
URL = "https://balme.ug.edu.gh/past.exampapers/index.php?p=member"
USER_NAME = os.environ.get("USER_NAME")
PASSWORD = os.environ.get("PASSWORD")


# Logging setup
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s: %(message)s")

# Deployed Selenium Setup
try:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    PATH = "/tmp"
    PROFILE = {
        "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
        "download.default_directory": PATH,
        "download.extensions_to_open": "",
    }  # Open externally not with chrome's pdf viewer
    chrome_options.add_experimental_option("prefs", PROFILE)
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options
    )
    logging.info("Setup successfully completed.")
except:
    logging.critical("Failed to set up selenium")
    sys.exit("Error setting up selenium.")


# Log in
try:
    driver.get(URL)
    username_field = driver.find_element(By.NAME, "memberID")
    password_field = driver.find_element(By.NAME, "memberPassWord")
    login_button = driver.find_element(By.NAME, "logMeIn")
    username_field.send_keys(USER_NAME)  # The newline is interpreted as enter
    password_field.send_keys(PASSWORD)
    login_button.click()
    logging.info("Logged in successfully, waiting for user input...")
except:
    logging.critical("Failed to log in.")
    sys.exit("Error logging in.")


def get_latest_past_question_path(path: str) -> str:
    """
    A function that returns the path of the downloaded file.
    It checks the past questions directory and returns the most recent one.
    """
    logging.info("Checking path for latest file.")
    files = os.listdir(path)
    pdfs = [
        os.path.join(path, basename) for basename in files if basename.endswith(".pdf")
    ]

    latest_file = max(pdfs, key=os.path.getctime)
    logging.info("Retrieved latest file successfully.")
    return latest_file


def search_for_past_question(cleaned_pasco_name: str) -> int:
    """
    A function to search for past question.
    It takes in the concatenated course name and course code.

    Returns 0 if it was able to search.
    Returns 1 if there was an error encountered.

    """
    logging.info(
        f"Searching for {cleaned_pasco_name}: The current_url is {driver.current_url}")
    try:
        search_field = driver.find_element(By.NAME, "keywords")
        search_button = driver.find_element(By.NAME, "search")
        # Double Quotes give accurate queries
        search_field.send_keys(f'"{cleaned_pasco_name}"')
        search_button.click()
        logging.info("Search was clicked successfully.")
        logging.info(
            f"After searching for {cleaned_pasco_name}: The current_url is {driver.current_url}")
        return 0
    except:
        logging.error(
            "Failed to search for {cleaned_pasco_name}", exc_info=True)
        return 1


def get_list_of_past_question() -> List[str]:
    """
    A function to retrieve the names, year and semester of
    past questions displayed.

    output: A print-out of the name, year and semester of
                    past question.
    """

    filtered_past_question_list = []
    logging.info(
        f"Retrieving list of past question: The current_url is {driver.current_url}")

    try:
        past_question_page = requests.get(driver.current_url)
        past_question_content = BeautifulSoup(
            past_question_page.content, "lxml")
        past_question_list = past_question_content.find_all(
            "div", class_="item biblioRecord")
        logging.info("Got list of past questions successfully.")
    except:
        logging.error("Failed to find past questions.", exc_info=True)
        return filtered_past_question_list
    else:
        if past_question_list:
            for past_question in past_question_list:
                past_question_title = past_question.find(
                    "a", class_="titleField")
                past_question_year = past_question.find(
                    "div", class_="customField isbnField")
                past_question_semester = past_question.find(
                    "div", class_="customField collationField")
                filtered_past_question_list.append(
                    past_question_title.get_text()
                    + "\n"
                    + past_question_year.get_text()
                    + "\n"
                    + past_question_semester.get_text()
                )
        logging.info(
            "Appeneded key aspects of past questions to filtered list successfully.")
        return filtered_past_question_list


def get_links_of_past_question() -> Dict[int, Any]:
    """
    A function to retrieve the links of all the past questions displayed.

    output: A dictionary containing the index and the past question link.
    """
    past_question_links = {}
    logging.info(
        f"Retrieving links of past question: The current_url is {driver.current_url}")

    try:
        past_question_page = requests.get(driver.current_url)
        past_question_content = BeautifulSoup(
            past_question_page.content, "lxml")
        past_question_list = past_question_content.find_all(
            "a", class_="titleField")
        logging.info("Retrieved past question links successfully.")
    except:
        logging.error(
            "Failed to extract links of past questions.", exc_info=True)
        return past_question_links
    else:
        for past_question_index in range(1, len(past_question_list) + 1):
            past_question_links[past_question_index] = (
                "https://balme.ug.edu.gh"
                + past_question_list[past_question_index - 1]["href"]
            )
        logging.info("Extracted past question links successfully.")

        return past_question_links


def get_past_question(past_question_links: Dict[int, Any], choice: int) -> str:
    """
    A function to download past questions.
    It takes in the links of the past questions and the users choice.
    Returns the path of the downloaded past question.

    """
    # chat_id = get_chat_id()
    # dir = os.getcwd()+f"files\{str(chat_id)}"
    # if not os.path.exists(dir):
    #     os.mkdir(dir)
    # os.chdir(dir)

    for index, past_question_link in past_question_links.items():
        if int(choice) == index:
            driver.get(past_question_link)  # Move to the url of users choice.
            logging.info(f"Moved to {past_question_link} successfully.")
            break

    logging.info(
        f"Downloading past question: The current_url is {driver.current_url}")
    file = driver.find_element(By.CLASS_NAME, "openPopUp")
    driver.execute_script(
        "arguments[0].click();", file
    )  # screen displayed is a frame, so adapts to a frame.
    wait = WebDriverWait(driver, 10)
    wait.until(EC.frame_to_be_available_and_switch_to_it(
        (By.CLASS_NAME, "cboxIframe")))
    wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()

    logging.info("Downloading file...")
    driver.back()
    # TODO: wait for file to be downloaded before moving on. latency fix
    time.sleep(2)
    past_question_file = get_latest_past_question_path(PATH)
    return past_question_file


def get_all_past_questions(past_question_links: Dict[int, Any]) -> str:
    pass


if __name__ == "__main__":
    name = input("Please enter the course name : ")
    search_for_past_question(name)
    questions = get_list_of_past_question()
    pasco_links = get_links_of_past_question()
    user_choice = input("Number please: ")
    get_past_question(pasco_links, user_choice)
