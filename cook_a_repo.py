#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from config import USERNAME, PASSWORD
import sys
import pyperclip


# Check if the repository name is provided as a command-line argument
if len(sys.argv) < 2:
    print('Please provide the repo name as an argument.')
    sys.exit()

repo_name = sys.argv[1]

# Check if the visibility argument is provided as a command-line argument
if len(sys.argv) >= 3 and sys.argv[2] in ['public', 'private']:
    visibility = sys.argv[2]
else:
    visibility = 'public'



options = webdriver.ChromeOptions()
options.add_argument('--headless') 
options.add_experimental_option("detach", True)


# Specify the path to the ChromeDriver executable
chromedriver_path = "/Users/kalinduadikari/Downloads/newcdriver/chromedriver_mac_arm64/chromedriver"

# Create a Service object
service = Service(executable_path=chromedriver_path)

# Pass the Service object and options when creating the WebDriver
browser = webdriver.Chrome(service=service, options=options)

browser.get("https://github.com/login")

# Find the login elements
username_input = browser.find_element(By.ID, "login_field")
password_input = browser.find_element(By.ID, "password")
login_button = browser.find_element(By.NAME, "commit")

# Replace 'USERNAME' and 'PASSWORD' with your GitHub credentials
username_input.send_keys(USERNAME)
password_input.send_keys(PASSWORD)
login_button.click()

browser.get("https://github.com/new")

# Find the input field by its ID and set the repository name
name_field = browser.find_element(By.ID, "react-aria-3")
name_field.clear()
name_field.send_keys(repo_name)

# Find the visibility radio button by its XPath and click based on the provided visibility argument
visibility_radio_button = browser.find_element(By.XPATH, f'//input[@type="radio" and @name="visibilityGroup" and @value="{visibility}"]')
visibility_radio_button.click()

# Wait for the 'Create repository' button to be clickable
try:
    wait = WebDriverWait(browser, 10)
    create_repo_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@data-no-visuals="true" and descendant::span[text()="Create repository"]]')))
except TimeoutException:
    print("Timeout: The 'Create repository' button is not clickable.")
    browser.quit()
    sys.exit()

# Introduce a short sleep to ensure the button is ready to be clicked
time.sleep(1)  # Adjust the sleep time as needed

# Use Selenium's built-in click() method to click the button
try:
    create_repo_button.click()
except Exception as e:
    print(f"Error clicking the 'Create repository' button: {e}")


# Introduce a short sleep after creating the repository to ensure the clipboard button is ready to be clicked
time.sleep(1)  # Adjust the sleep time as needed


# Wait for the repository to be created and the URL to appear
try:
    wait = WebDriverWait(browser, 20)  # Increase the wait time if needed
    github_url_element = wait.until(EC.presence_of_element_located((By.XPATH, "//clipboard-copy[@for='empty-setup-clone-url']")))
    # Extract the GitHub URL from the data-hydro-click attribute
    #github_url = github_url_element.get_attribute("data-hydro-click")
    #github_url = github_url.split('"originating_url":"')[1].split('"')[0]
    #print("GitHub URL:", github_url)
    print(f'Github URL: https://github.com/Kalinduadikari/{repo_name}.git')
except TimeoutException:
    print("Timeout: GitHub URL not found.")
    print("Error!! : Repo name gotta be unique dude!!")  # Display custom error message if the GitHub URL is not found
    browser.quit()
    sys.exit()
except Exception as e:
    print("Error while getting the GitHub URL:", e)
    print("Error!! : Repo name gotta be unique dude!!")  # Display custom error message for any other errors