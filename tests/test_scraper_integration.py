"""Integration Tests."""

import pytest
from helpers import check_for_pdf, count_pdfs_in_path

from functions import Functions

search_term = "Math 121"


@pytest.mark.integration
def test_get_list_of_past_questions_integration():
    """Test if the bot can get the list of past questions."""
    scraper = Functions()
    scraper.search_for_past_question(search_term)
    past_questions_dict = scraper.get_list_of_past_question()
    assert past_questions_dict


@pytest.mark.integration
def test_get_links_of_past_questions_integration():
    """Test if the bot can get the links of past questions."""
    scraper = Functions()
    scraper.search_for_past_question(search_term)
    past_questions_links_dict = scraper.get_links_of_past_question()
    assert past_questions_links_dict


@pytest.mark.integration
def test_get_past_question_integration():
    """Test if the bot can get a past question."""
    scraper = Functions()
    scraper.search_for_past_question(search_term)
    past_question_links_dict = scraper.get_links_of_past_question()
    print(past_question_links_dict)
    next(scraper.get_past_question(past_question_links_dict, 1))
    assert check_for_pdf(scraper.path) is True
    assert count_pdfs_in_path(scraper.path) == 1
