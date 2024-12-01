import os
from time import sleep
from threading import Thread

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions

import importlib
import pytest

from todo_app import create_app
from dotenv import find_dotenv, load_dotenv
import todo_app.data.cosmos_client


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Use our test integration config instead of the 'real' version
    file_path = find_dotenv('./.env.local')
    load_dotenv(file_path, override=True)
    importlib.reload(todo_app.data.cosmos_client)

    # Construct the new application
    application = create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    # Give the app a moment to start
    sleep(1)

    yield application

    # Tear Down
    thread.join(1)


@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome(options=opts) as driver:
        yield driver


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')

    driver.find_element(by=By.ID, value="title").send_keys("Test title")
    driver.find_element(by=By.ID, value="description").send_keys("Test description")
    driver.find_element(by=By.ID, value="due-date").send_keys("01/01/2025")
    driver.find_element(by=By.ID, value="new-todo-submit").click()

    assert driver.title == "To-Do App"
    wait = WebDriverWait(driver, 5)
    wait.until(
        lambda inner_driver: expected_conditions.all_of(
            expected_conditions.text_to_be_present_in_element((By.ID, "todos"),"Test title"),
            expected_conditions.text_to_be_present_in_element((By.ID, "todos"), "Not Started"),
        )
    )

    complete_button = driver.find_element(by=By.ID, value="complete-todo")
    complete_button.click()
    wait.until(
        lambda inner_driver: expected_conditions.text_to_be_present_in_element((By.ID, "todos"), "Completed")
    )

    uncomplete_button = driver.find_element(by=By.ID, value="uncomplete-todo")
    uncomplete_button.click()
    wait.until(
        lambda inner_driver: expected_conditions.text_to_be_present_in_element((By.ID, "todos"), "Not Started")
    )

    delete_button = driver.find_element(by=By.ID, value="delete-todo")
    delete_button.click()
    wait.until(
        lambda inner_driver: expected_conditions.none_of(
            expected_conditions.text_to_be_present_in_element((By.ID, "todos"), "Test title"),
        )
    )
