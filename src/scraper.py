"""Scraper."""

import logging
import logging.config
import os
import re
import time
import traceback
from typing import Dict, Generator, List, Union

import dotenv
import requests
# Polling Selenium setup
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchAttributeException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.path_separator import get_file_separator

# Constants
dotenv.load_dotenv()
URL = os.getenv("URL")
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


class Scraper:
    """Functions class."""




    def __init__(self) -> None:
        """Initializes a headless chrome browser and logs in to a website."""
        self.logged_in = False
        self.path = (
            os.getcwd() + get_file_separator() + "src" + get_file_separator() + "tmp"
        )
        self.CURRENT_UUID = "CURRENT_UUID"
        s = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # Open externally not with chrome's pdf viewer
        self.PROFILE = {
            "plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}],
            "download.default_directory": self.path,
            "download.extensions_to_open": "",
        }
        # options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        options.add_experimental_option("prefs", self.PROFILE)
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # self.driver = webdriver.Chrome(
        #     executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options
        # )
        self.driver = webdriver.Chrome(service=s, options=options)
        self.driver.implicitly_wait(6)

        # Log in
        try:
            self.driver.get(URL)

            username_field = self.driver.find_element(By.NAME, "memberID")
            password_field = self.driver.find_element(By.NAME, "memberPassWord")

            username_field.send_keys(USERNAME)
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.ENTER)

            self.driver.find_element(By.ID, "memberLogout")
            self.logged_in = True

        except (NoSuchElementException, NoSuchAttributeException):
            print("Failed to log in.", exc_info=True)
        except Exception:
            print("Error occurred while logging in.")
