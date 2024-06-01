# web_search.py

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time

def open_browser_and_search(search_for):
    # Base URL for Google
    url = "https://www.google.com/search?q=" + search_for
    # Initialize the Firefox webdriver
    driver = webdriver.Firefox()  # Assumes geckodriver is in PATH
    # Open the constructed Google search URL
    driver.get(url)
    
    try:
        # Wait until the browser window is closed by the user
        while True:
            try:
                if not driver.window_handles:
                    break
            except WebDriverException:
                # Handle the case where the browser window is already closed
                break
            time.sleep(1)
    finally:
        driver.quit()