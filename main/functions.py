"""Functions file."""
import logging
import logging.config
import os
import re
import time
import traceback
from typing import Dict, Generator, List, Union

import dotenv
import requests
import utils.uuid as uuid
# Polling Selenium setup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchAttributeException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
# Used when polling.
from webdriver_manager.chrome import ChromeDriverManager

# Logging setup
logging.config.fileConfig(
    fname="log.ini",
    disable_existing_loggers=False,
)
logger = logging.getLogger(__name__)
file_logger = logging.getLogger("fileLogger")


# Constants
dotenv.load_dotenv()
URL = os.getenv("URL")
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
CHROME_DRIVER_LOCAL_PATH = os.getenv("CHROME_DRIVER_LOCAL_PATH")
CHROME_DRIVER_RENDER_PATH = os.getenv("CHROME_DRIVER_RENDER_PATH")


class Functions:
    """Functions class."""

    def __init__(self, path):
        """Initializes a headless chrome browser and logs in to a website.

        Args:
          path: the path to the directory where the pdf's will be downloaded
        """
        self.logged_in = False
        self.path = path
        self.CURRENT_UUID = "CURRENT_UUID"
        # s = Service(ChromeDriverManager().install())
        #s = Service("/opt/render/project/src/main/chromedriver.exe")
        # s = Service(CHROME_DRIVER_RENDER_PATH)

        options = webdriver.ChromeOptions()
        # Open externally not with chrome's pdf viewer
        self.PROFILE = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": path,
            "download.extensions_to_open": "",
        }
        options.add_experimental_option("prefs", self.PROFILE)
        options.add_argument("no-sandbox")
        # options.add_argument("headless")
        options.add_argument("disable-dev-shm-usage")
        options.add_argument("force-dark-mode")
        options.add_argument("start-maximized")
        options.add_argument("disable-gpu")
        # options.binary_location = os.getcwd() + CHROME_DRIVER_RENDER_PATH
        options.binary_location = "/opt/render/project/.render/chrome/opt/google/chrome/google-chrome"
        options.add_argument("disable-extensions")
        options.add_argument("disable-infobars")
        print(os.getcwd())
        self.driver = webdriver.Chrome(executable_path=CHROME_DRIVER_RENDER_PATH, options=options)

        # Log in
        try:
            self.driver.get(URL)
            username_field = self.driver.find_element(By.NAME, "memberID")
            password_field = self.driver.find_element(By.NAME, "memberPassWord")
            login_button = self.driver.find_element(By.NAME, "logMeIn")
            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            login_button.click()
            logger.info("Logged in successfully, waiting for user input...")
            self.logged_in = True
        except (NoSuchElementException, NoSuchAttributeException):
            logger.critical("Failed to log in.", exc_info=True)
        except Exception:
            logger.exception("Error occurred while logging in.")

    def get_past_question_path(self, chat_id: str, path: str) -> Union[str, None]:
        """It takes a path as an argument, checks if there are any pdf files in the path, and if there are, it returns the most recent file in the path, if they aren't it returns None.

        Args:
          path (str): The path to the directory where the file is located.

        Returns:
          The path of the latest file in the directory.
        """
        logger.info("Checking path for latest file.")
        path_directory = os.listdir(self.path)
        user_file_path = [
            os.path.join(path, basename)
            for basename in path_directory
            if basename.endswith(".pdf")
        ]
        if len(user_file_path) == 0:
            return None
        user_file = max(user_file_path, key=os.path.getctime)
        file_logger.info(f"Downloaded file from path {user_file} has been uploaded to user.")
        file_logger.info("")

        return user_file


    def rename_past_question_file(self, chat_id: str):
        """It takes a file path and renames the file to the first 20 characters of the file name.

        Args:
          pasco_directory: The directory where the past questions are stored.
          file_path: The path to the file that you want to rename.

        Returns:
          The new path of the file.
        """
        new_uuid = uuid.generate_6_digits_uuid()
        self.CURRENT_UUID = new_uuid

        path_directory = os.listdir(self.path)
        absolute_path_directory = [
            os.path.join(self.path, basename)
            for basename in path_directory
            if basename.endswith(".pdf")
        ]
        user_file_path = sorted(
            absolute_path_directory, key=os.path.getctime, reverse=True
        )
        for file in user_file_path:
            if chat_id[:7] in file:
                continue
            # downloaded_file_path = max(absolute_path_directory, key=os.path.getctime)
            file_name = os.path.basename(file)
            new_path = f"{self.path}\\{chat_id}_{self.CURRENT_UUID}_{file_name[:9]}.pdf"
            os.replace(file, new_path)

            return new_path

    def search_for_past_question(self, cleaned_pasco_name: str) -> int:
        """It searches for a past question on the website, and returns 0 if it was successful, and 1 if it wasn't.

        Args:
          cleaned_pasco_name (str): The name of the file you're searching for.

        Returns:
          The return value is the status code of the function.
        """
        logger.info(
            f"Searching for {cleaned_pasco_name}: The current_url is {self.driver.current_url}"
        )
        file_logger.info(f"User has requested for {cleaned_pasco_name} past question.")
        try:
            search_field = self.driver.find_element(By.NAME, "keywords")
            search_button = self.driver.find_element(By.NAME, "search")
            # Double Quotes give accurate queries
            search_field.send_keys(f'"{cleaned_pasco_name}"')
            search_button.click()
            logger.info(
                f"After searching for {cleaned_pasco_name}: The current_url is {self.driver.current_url}"
            )
            return 0
        except (NoSuchElementException, NoSuchAttributeException):
            logger.exception("Search field and search button not found.")
            return 1
        except Exception:
            logger.exception(f"Failed to search for {cleaned_pasco_name}")
            return 1

    def get_list_of_past_question(self) -> List[str]:
        """
        It retrieves the names, year and semester of past questions displayed then adds them to a list.

        Returns:
          A list of strings.
        """
        filtered_past_question_list: List[str] = []
        logger.info(f"Retrieving list of past question from {self.driver.current_url}")

        try:
            past_question_page = requests.get(self.driver.current_url)
            past_question_content = BeautifulSoup(past_question_page.content, "lxml")
            past_question_list = past_question_content.find_all(
                "div", class_="item biblioRecord"
            )
            logger.info("Got list of past questions successfully.")
        except (NoSuchElementException, NoSuchAttributeException):
            logger.exception("Past question content field not found.")
            return filtered_past_question_list
        except Exception:
            logger.exception("Failed to retrieve past questions.")
            return filtered_past_question_list
        else:
            if past_question_list:
                for past_question in past_question_list:
                    past_question_title = past_question.find("a", class_="titleField")
                    past_question_year = past_question.find(
                        "div", class_="customField isbnField"
                    )
                    past_question_semester = past_question.find(
                        "div", class_="customField collationField"
                    )
                    filtered_past_question_list.append(
                        past_question_title.get_text()
                        + "\n"
                        + past_question_year.get_text()
                        + "\n"
                        + past_question_semester.get_text()
                    )
            logger.info(
                "Appended key aspects of past questions to filtered list successfully."
            )
            return filtered_past_question_list

    def past_question_list_to_string(self, list_of_values: List[str]) -> str:
        """It takes a list of strings, and returns a string with each item in the list on a new line, with a number in front of it.

        Args:
          list_of_values (List[str]): List[str]

        Returns:
          A string
        """
        updated_list = []
        for value in range(len(list_of_values)):
            updated_list.append(
                f"{value+1}. " + re.sub("\n", ", ", list_of_values[value])
            )
            updated_list.append("")

        modified_text = "\n".join(value for value in updated_list)

        return modified_text

    def get_links_of_past_question(self) -> Dict[int, str]:
        """
        It gets the links of past questions from the current page.

        Returns:
          A dictionary of past question links.
        """
        past_question_links: Dict[int, str] = {}
        logger.info(f"Retrieving links of past question from {self.driver.current_url}")

        try:
            past_question_page = requests.get(self.driver.current_url)
            past_question_content = BeautifulSoup(past_question_page.content, "lxml")
            past_question_list = past_question_content.find_all(
                "a", class_="titleField"
            )
            logger.info("Retrieved past question links successfully.")
        except (NoSuchElementException, NoSuchAttributeException):
            logger.exception("Past question link field not found.")
            return past_question_links
        except Exception:
            logger.exception(
                f"Failed to extract links of past questions. {traceback.format_exc()}"
            )
            return past_question_links
        else:
            for past_question_index in range(1, len(past_question_list) + 1):
                past_question_links[past_question_index] = (
                    "https://balme.ug.edu.gh"
                    + past_question_list[past_question_index - 1]["href"]
                )
            logger.info("Extracted past question links successfully.")

            return past_question_links

    def get_past_question(
        self, chat_id: str, past_question_links: Dict[int, str], choice: int
    ) -> Generator:
        """It takes in a dictionary of past question links and a choice from the user, then it moves to the url of the users choice and downloads the past question.

        Args:
          past_question_links (Dict[int, Any]): This is a dictionary of the past questions links.
          choice (int): The choice of the user.

        Returns:
          The path to the past_question_file
        """
        if int(choice) == -1:
            for past_question_link in past_question_links.values():
                self.driver.get(past_question_link)
                logger.info(f"Moved to {past_question_link} successfully.")
                self.download_past_question(chat_id, past_question_link)
                time.sleep(2)
                yield self.get_past_question_path(chat_id, self.path)
        else:
            for index, past_question_link in past_question_links.items():
                if int(choice) == index:
                    self.driver.get(
                        past_question_link
                    )  # Move to the url of users choice.
                    logger.info(f"Moved to {past_question_link} successfully.")

                    self.download_past_question(chat_id, past_question_link)
                    time.sleep(2)
                    yield self.get_past_question_path(chat_id, self.path)
                    break

    def download_past_question(self, chat_id, past_question_link) -> None:
        """Clicks on a button that opens a frame, then clicks on a button in the frame to download a file."""
        logger.info(f"Downloading past question from {self.driver.current_url}")
        try:
            file = self.driver.find_element(By.CLASS_NAME, "openPopUp")
            self.driver.execute_script(
                "arguments[0].click();", file
            )  # screen displayed is a frame, so adapts to a frame.
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe"))
            )
            wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()

            logger.info("Downloading file...")
            file_logger.info(f"{past_question_link} has been downloaded.")
            self.driver.back()
            time.sleep(2)
            self.rename_past_question_file(chat_id)
        except (NoSuchElementException, NoSuchAttributeException):
            logger.exception("Failed to find download button.")
            raise
        except TimeoutException:
            logger.exception("Timeout waiting for frame to load.")
            raise
        except Exception:
            logger.exception("Error occurred while downloading file.")
            raise


if __name__ == "__main__":
    function_class = Functions(str(os.getcwd()))
    name = input("Please enter the course name : ")
    function_class.search_for_past_question(name)
    questions = function_class.get_list_of_past_question()
    pasco_links = function_class.get_links_of_past_question()
    user_choice = int(input("The number of the past question you want to download: "))
    function_class.get_past_question(pasco_links, user_choice)
