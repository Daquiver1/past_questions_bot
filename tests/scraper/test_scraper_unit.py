"""Unit Tests."""

import os

import pytest
from bs4 import BeautifulSoup

from functions import Functions

search_term = "Math 121"


@pytest.mark.unit
def test_is_logged_in_unit():
    """Test if the bot is logged in."""
    scraper = Functions()
    assert scraper.logged_in is True


@pytest.mark.unit
def test_search_functionality_unit():
    """Test if the bot can search for past questions."""
    scraper = Functions()
    scraper.search_for_past_question(search_term)
    assert search_term in scraper.driver.page_source


@pytest.mark.parametrize(
    ("page_content,expected_values"),
    [
        ("", {}),
        (
            """<a href="/past.exampapers/index.php?p=show_detail&amp;id=9731&amp;keywords=%22math+121%22" class="titleField" itemprop="name" property="name" title="View record detail description for this title"><span class="highlight">MATH 121</span>: Algebra And Trigonometry</a>""",
            {
                1: "https://balme.ug.edu.gh/past.exampapers/index.php?p=show_detail&id=9731&keywords=%22math+121%22"
            },
        ),
    ],
)
@pytest.mark.unit
def test_get_links_of_past_questions_unit(page_content, expected_values, monkeypatch):
    """Test if the bot can get the links of past questions."""
    scraper = Functions()

    mock_url = "http://test.url"
    monkeypatch.setattr(scraper, "driver", type("", (), {"current_url": mock_url}))

    mock_content = page_content

    monkeypatch.setattr(
        "requests.get", lambda url: type("", (), {"content": mock_content})
    )
    monkeypatch.setattr("bs4.BeautifulSoup", BeautifulSoup)

    result = scraper.get_links_of_past_question()
    assert len(result) == len(expected_values)
    if len(expected_values) > 0:
        assert result[1] == expected_values[1]


@pytest.mark.parametrize(
    "page_content,expected_values",
    [
        (
            "",
            {0: ""},
        ),
        (
            """<div class="item biblioRecord">
        <a class="titleField">Test Title</a>
        <div class="customField isbnField">Test Year</div>
        <div class="customField collationField">Test Semester</div>
    </div>""",
            {1: "Test Title\nTest Year\nTest Semester"},
        ),
    ],
)
@pytest.mark.unit
def test_get_list_of_past_questions_unit(page_content, expected_values, monkeypatch):
    """Test if the bot can get the list of past questions."""
    scraper = Functions()
    mock_url = "http://test.url"
    monkeypatch.setattr(scraper, "driver", type("", (), {"current_url": mock_url}))

    mock_content = page_content

    monkeypatch.setattr(
        "requests.get", lambda url: type("", (), {"content": mock_content})
    )
    monkeypatch.setattr("bs4.BeautifulSoup", BeautifulSoup)

    result = scraper.get_list_of_past_question()
    key = next(iter(expected_values))
    assert len(result) == key
    if (
        key > 0
    ):  # Key stores the length of the list, so subtract by 1 to bypass off by one error.
        assert result[key - 1] == expected_values[key]


@pytest.mark.parametrize(
    "search_term,expected_values",
    [
        ("https://google.com", False),
        (
            "https://balme.ug.edu.gh/past.exampapers/index.php?p=show_detail&id=8831&keywords=%22Math+126%22",
            True,
        ),
    ],
)
@pytest.mark.unit
def test_download_past_question_unit(search_term, expected_values):
    """Test if the bot can download past questions."""
    scraper = Functions()
    scraper.driver.get(search_term)

    result = scraper.download_past_question()
    assert result is expected_values


@pytest.mark.parametrize(
    "files_in_path,expected_values",
    [
        (["file1.pdf", "file2.pdf", "file3.txt"], "/mock/path\\file2.pdf"),
        (["file1.txt", "file2.txt"], None),
    ],
)
@pytest.mark.unit
def test_get_past_question_path_unit(files_in_path, expected_values, monkeypatch):
    """Test if the bot can get the path of the past question."""
    monkeypatch.setattr(os, "listdir", lambda path: files_in_path)
    monkeypatch.setattr(
        os.path,
        "getctime",
        lambda path: {"file1.pdf": 1, "file2.pdf": 2, "file3.txt": 3}[
            os.path.basename(path)
        ],
    )

    scraper = Functions()

    result = scraper.get_past_question_path("/mock/path")
    assert result == expected_values
