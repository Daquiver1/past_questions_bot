"""A module to scrape past questions from the balme library portal."""

import os
import time

import dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC # noqa
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

dotenv.load_dotenv()
URL = os.getenv("URL")
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


class Scraper:
    """A class to scrape past questions from the balme library portal."""

    def __init__(self, year: str) -> None:
        """Initialize the scraper."""
        self.year = year
        self.driver = self._setup_driver()
        self._login()

    def _setup_driver(self) -> webdriver.Chrome:
        """Setup the chrome driver."""
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "plugins.plugins_list": [
                    {"enabled": False, "name": "Chrome PDF Viewer"}
                ],
                "download.default_directory": os.getcwd()
                + os.sep
                + "src"
                + os.sep
                + "tmp",
                "download.extensions_to_open": "",
            },
        )
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        s = webdriver.ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=s, options=options)

    def _login(self) -> None:
        """Login to the balme library portal."""
        self.driver.get(URL)
        try:
            self.driver.find_element(By.NAME, "memberID").send_keys(USERNAME)
            password_field = self.driver.find_element(By.NAME, "memberPassWord")
            password_field.send_keys(PASSWORD)
            password_field.send_keys(Keys.ENTER)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "memberLogout"))
            )
            print("Successfully logged in.")
            return True
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def get_new_downloads(
        self, directory: str, start_time: int, timeout: int = 30
    ) -> list:
        """Wait for new files to appear in the directory that were downloaded after `start_time`."""
        sleep_interval = 1
        elapsed_time = 0
        new_files = []

        while elapsed_time < timeout:
            for file in os.listdir(directory):
                file_path = os.path.join(directory, file)
                if os.path.getctime(
                    file_path
                ) > start_time.timestamp() and file.endswith(".pdf"):
                    new_files.append(file_path)
            if new_files:  # If you've found new files, return them
                return new_files
            time.sleep(sleep_interval)
            elapsed_time += sleep_interval

        raise TimeoutError(
            f"No new files appeared in {directory} after {timeout} seconds."
        )

    def get_most_recent_file(self, directory: str, extension: str) -> str:
        """Get the path of the most recently downloaded file with a specific extension."""
        try:
            files = [
                os.path.join(directory, f)
                for f in os.listdir(directory)
                if f.endswith(extension)
            ]
            latest_file = max(files, key=os.path.getmtime)
            return latest_file
        except ValueError:  # If the directory is empty
            return None

    def sanitize_filename(self, filename: str) -> str:
        """Remove or replace characters that are not allowed in Windows filenames."""
        return (
            filename.replace(":", "_")
            .replace("\\", "_")
            .replace("/", "")
            .replace("*", "_")
            .replace("?", "_")
            .replace('"', "_")
            .replace("<", "_")
            .replace(">", "_")
            .replace("|", "_")
            .replace(" ", "")
        )

    def process_downloaded_file(self, file_path: str, details: dict) -> None:
        """Add specific metadata to the downloaded file."""
        print(details)
        sanitized_title = self.sanitize_filename(details["title"][:8])
        sanitized_year = self.sanitize_filename(
            details["year"]
        )  # Extracts the year number
        sanitized_semester = self.sanitize_filename(
            details["semester"]
        )  # Extracts the semester
        new_filename = f"{sanitized_title}_{sanitized_year}_{sanitized_semester}.pdf"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        os.rename(file_path, new_file_path)

    def search_past_questions(self) -> None:
        """Search for past questions."""
        try:
            self.driver.find_element(By.CLASS_NAME, "s-search-advances").click()
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "advance-search"))
            )
            advanced_section = self.driver.find_element(By.ID, "advance-search")
            advanced_section.find_element(By.NAME, "isbn").send_keys(self.year)
            advanced_section.find_element(By.NAME, "search").click()
            print(f"Searched for past questions for the year {self.year}.")
        except Exception as e:
            print(f"Error during search: {e}")

    def get_past_questions_details_and_links(self) -> dict:
        """Get the details and links of the past questions."""
        past_questions_details = {}
        try:
            html_content = self.driver.page_source
            past_question_content = BeautifulSoup(html_content, "lxml")

            past_question_items = past_question_content.find_all(
                "div", class_="item biblioRecord"
            )

            for index, item in enumerate(past_question_items, start=1):
                title_element = item.find("a", class_="titleField")
                title = (
                    title_element.get_text(strip=True)[:8]
                    if title_element
                    else "No title found"
                )
                year_element = item.find("div", class_="customField isbnField")
                year = (
                    year_element.get_text(strip=True)[18:]
                    if year_element
                    else "No year found"
                )
                semester_element = item.find("div", class_="customField collationField")
                semester = (
                    semester_element.get_text(strip=True)[10:]
                    if semester_element
                    else "No semester found"
                )
                link = (
                    "https://balme.ug.edu.gh" + title_element["href"]
                    if title_element and title_element.has_attr("href")
                    else "No link found"
                )

                past_questions_details[index] = {
                    "title": title,
                    "year": year,
                    "semester": semester,
                    "link": link,
                }
        except Exception as e:
            print(f"Error retrieving past questions details and links: {e}")

        return past_questions_details

    def download_past_questions(self, past_questions_details: dict) -> None:
        """Download the past questions and process them."""
        download_directory = os.getcwd() + os.sep + "src" + os.sep + "tmp"
        for _, details in past_questions_details.items():
            self.download_and_process_question(details, download_directory)

    def download_and_process_question(
        self, details: dict, download_directory: str
    ) -> None:
        """Download the past questions."""
        link = details.get("link")
        if link:
            try:
                self.driver.get(link)
                file = self.driver.find_element(By.CLASS_NAME, "openPopUp")
                self.driver.execute_script("arguments[0].click();", file)
                WebDriverWait(self.driver, 15).until(
                    EC.frame_to_be_available_and_switch_to_it(
                        (By.CLASS_NAME, "cboxIframe")
                    )
                )
                time.sleep(3)
                download_button = WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.ID, "download"))
                )
                download_button.click()
                print(f"Initiated download for {details['title']}.")
                time.sleep(5)
                downloaded_file_path = self.get_most_recent_file(
                    download_directory, ".pdf"
                )
                if downloaded_file_path:
                    self.process_downloaded_file(downloaded_file_path, details)
            except TimeoutException:
                print(f"Timeout occurred trying to download from {link}.")
            except NoSuchElementException:
                print(f"Download button not found for {link}.")
            except Exception as e:
                print(f"Error during download from {link}: {e}")
        else:
            print(f"No download link found for past question {details['title']}.")


if __name__ == "__main__":
    scraper = Scraper("1996")
    scraper.search_past_questions()
    links = scraper.get_past_questions_details_and_links()
    scraper.download_past_questions(links)
    time.sleep(200)
