"""Functions file."""
import logging
import logging.config
import os
import re
import time
import traceback
from typing import Dict, List, Union

import requests


from past_question_bot.constant import URL, USERNAME, PASSWORD

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchAttributeException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger("helpers")


class Scrapper:

    def __init__(self, path):
        self.logged_in = False
        self.path = path
        s = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()

        self.PROFILE = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": path, #Emile: path to save file
            "download.extensions_to_open": "",
        }

        options.add_experimental_option("prefs", self.PROFILE)
        
        self.driver = webdriver.Chrome(service=s, options=options)

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

    def get_past_question_path(self, path: str) -> Union[str, None]:
        logger.info("Checking path for latest file.")
        file_path = os.listdir(path)

        user_file_path = [
            os.path.join(path, basename)
            for basename in file_path
            if basename.endswith(".pdf")
        ]
        if len(user_file_path) == 0:
            return None

        new_file_path = max(user_file_path, key=os.path.getctime)
        logger.info(
            f"Downloaded file from path {new_file_path} has been uploaded to user."
        )
        logger.info("")
        return new_file_path


    def rename_past_question_file(self, pasco_directory, file_path):
        file_name = os.path.basename(file_path)
        new_path = f"{pasco_directory} + \\ + {file_name[:20]}.pdf"
        os.rename(file_path, new_path)

        return new_path

    def is_new_file(self, path) -> bool:
        current_time = time.time()
        file_created_time = os.path.getctime(path)

        if (current_time - file_created_time) > 10:
            return False
        return True

    def search_for_past_question(self, cleaned_pasco_name: str) -> int:
        logger.info(
            f"Searching for {cleaned_pasco_name}: The current_url is {self.driver.current_url}"
        )
        logger.info(f"User has requested for {cleaned_pasco_name} past question.")
        try:
            search_field = self.driver.find_element(By.NAME, "keywords")
            search_button = self.driver.find_element(By.NAME, "search")
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
        updated_list = []
        for value in range(len(list_of_values)):
            updated_list.append(
                f"{value+1}. " + re.sub("\n", ", ", list_of_values[value])
            )
            updated_list.append("")

        modified_text = "\n".join(value for value in updated_list)

        return modified_text

    def get_links_of_past_question(self) -> Dict[int, str]:
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
        self, past_question_links: Dict[int, str], choice: int
    ) -> str:
        if int(choice) == -1:
            for past_question_link in past_question_links.values():
                self.driver.get(past_question_link)
                logger.info(f"Moved to {past_question_link} successfully.")
                self.download_past_question(past_question_link)
                yield self.get_past_question_path(self.path)
        else:
            for index, past_question_link in past_question_links.items():
                if int(choice) == index:
                    self.driver.get(
                        past_question_link
                    )
                    logger.info(f"Moved to {past_question_link} successfully.")

                    self.download_past_question(past_question_link)
                    yield self.get_past_question_path(self.path)
                    break

    def download_past_question(self, past_question_link) -> None:
        logger.info(f"Downloading past question from {self.driver.current_url}")
        try:
            file = self.driver.find_element(By.CLASS_NAME, "openPopUp")
            self.driver.execute_script(
                "arguments[0].click();", file
            )
            wait = WebDriverWait(self.driver, 10)
            wait.until(
                EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe"))
            )
            wait.until(EC.element_to_be_clickable((By.ID, "download"))).click()

            logger.info("Downloading file...")
            logger.info(f"{past_question_link} has been downloaded.")
            self.driver.back()
            time.sleep(2)
        except (NoSuchElementException, NoSuchAttributeException):
            logger.exception("Failed to find download button.")
            raise
        except TimeoutException:
            logger.exception("Timeout waiting for frame to load.")
            raise
        except Exception:
            logger.exception("Error occurred while downloading file.")
            raise


# Move to test
if __name__ == "__main__":
    function_class = Scrapper(str(os.getcwd()))
    name = input("Please enter the course name : ")
    function_class.search_for_past_question(name)
    questions = function_class.get_list_of_past_question()
    pasco_links = function_class.get_links_of_past_question()
    user_choice = int(input("The number of the past question you want to download: "))
    function_class.get_past_question(pasco_links, user_choice)
