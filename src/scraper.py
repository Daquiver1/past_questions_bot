"""A module to scrape past questions from the balme library portal."""

import os
import re
import time

import dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC  # noqa
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

dotenv.load_dotenv()
URL = os.getenv("URL")
USERNAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")


class Scraper:
    """A class to scrape past questions from the balme library portal."""

    def __init__(self, folder_name: str) -> None:
        """Initialize the scraper."""
        self.folder_name = folder_name
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
                + "past_questions"
                + os.sep
                + self.folder_name,
                "download.extensions_to_open": "",
            },
        )
        options.add_argument("--no-sandbox")
        options.add_argument("--headless=new")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-software-rasterizer")
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

    def extract_course_code(self, title_text: str) -> str:
        """Extract the course code from the title of a past question."""
        if title_text:
            # Adjusted regex pattern to be more inclusive and flexible with spaces and separators
            pattern = re.compile(r"\b([A-Za-z]{4})[\s\-:/]?(\d{3})\b")
            match = pattern.search(title_text)  # Use search to find the first match

            if match:
                # Format the match into the desired output: "PREFIX NUMBER"
                return f"{match.group(1)} {match.group(2)}"
            else:
                return None  # No valid course code found
        else:
            return None

    def extract_semester_text(self, semester_text: str) -> str:
        """Extract the semester from the semester text."""
        if semester_text:
            if "first" in semester_text.lower():
                return "First"
            elif "second" in semester_text.lower():
                return "Second"
            else:
                return "Supplementary"
        return "No Semester Found"

    def extract_year_text(self, year_text: str) -> str:
        """Extract the year from the year text."""
        if year_text:
            if "/" in year_text:
                return year_text.split("/")[-1].strip()
            else:
                return year_text
        else:
            return "No Year Found"

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
        sanitized_title = self.sanitize_filename(details["title"][:8])
        sanitized_year = self.sanitize_filename(details["year_of_examination"])
        sanitized_semester = self.sanitize_filename(details["semester"])
        new_filename = f"{details['id']}_{sanitized_title}_{sanitized_year}_{sanitized_semester}.pdf"
        new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
        if os.path.exists(new_file_path):
            print(f"File already exists: {new_file_path}. Skipping...")
        else:
            os.rename(file_path, new_file_path)
            print(f"Renamed {details['title']} successfully.")

    def download_past_question(self, past_questions_details: dict) -> None:
        """Download the past questions and process them."""
        download_directory = (
            os.getcwd() + os.sep + "past_questions" + os.sep + self.folder_name
        )
        self.download_and_process_question(past_questions_details, download_directory)

    def download_and_process_question(
        self, details: dict, download_directory: str
    ) -> None:
        """Download the past questions."""
        if details is None:
            return
        try:
            file = self.driver.find_element(By.CLASS_NAME, "openPopUp")
            self.driver.execute_script("arguments[0].click();", file)
            WebDriverWait(self.driver, 15).until(
                EC.frame_to_be_available_and_switch_to_it((By.CLASS_NAME, "cboxIframe"))
            )
            time.sleep(3)
            download_button = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "download"))
            )
            print(f"Initiated download for {details['title']}.")
            download_button.click()
            time.sleep(5)
            downloaded_file_path = self.get_most_recent_file(download_directory, ".pdf")
            if downloaded_file_path:
                print(f"{details['title']} downloaded successfully")
                self.process_downloaded_file(downloaded_file_path, details)
            else:
                print(f"File not found for {details['title']}.")
        except TimeoutException:
            print(f"Timeout occurred trying to download from {details['title']}.")
        except NoSuchElementException:
            print(f"Download button not found for {details['title']}.")
        except Exception as e:
            print(f"Error during download from {details['title']}: {e}")

    def get_past_question_details(self, id: str) -> None:
        """Get past questions details."""
        BASE_URL = (  # noqa
            f"https://balme.ug.edu.gh/past.exampapers/index.php?p=show_detail&id={id}"
        )
        self.driver.get(BASE_URL)

        try:
            html_content = self.driver.page_source
            soup = BeautifulSoup(html_content, "lxml")

            title_element = soup.find("a", class_="openPopUp")
            if title_element is None:
                return None
            title = self.extract_course_code(title_element.text.strip())
            if title is None:
                return None

            table = soup.find("table", class_="s-table")
            if table:
                semester_element = (
                    table.find("th", string="Semester")
                    .find_next_sibling("td")
                    .div.text.strip()
                )
                semester = self.extract_semester_text(semester_element)
                year_of_examination_element = (
                    table.find("th", string="Year of Examination")
                    .find_next_sibling("td")
                    .div.text.strip()
                )
                year_of_examination = self.extract_year_text(
                    year_of_examination_element
                )
            else:
                return None

            past_questions_details = {
                "id": id,
                "title": title,
                "semester": semester,
                "year_of_examination": year_of_examination,
            }
            return past_questions_details
        except Exception as e:
            print(f"Error retrieving past questions details: {e}")


if __name__ == "__main__":
    scraper = Scraper("twelve-set")
    ids = range(11000, 11737)

    for id in ids:
        details = scraper.get_past_question_details(str(id))
        scraper.download_past_question(details)

    # stat 334, arab 304, math 425 in 9ks
    # geog  403, adlt 202, adlt 048 in 11ks
    print("Done")
