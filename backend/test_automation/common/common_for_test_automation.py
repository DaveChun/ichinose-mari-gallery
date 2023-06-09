from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
import sys
from dotenv import load_dotenv
from time import sleep

# Absolute env path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(ROOT_DIR, '.env'))
parent_path = os.path.dirname(ROOT_DIR)
sys.path.append(os.path.dirname(parent_path))
from app import db

id = os.environ.get("ID_FOR_TESTING")
url = os.environ.get("TARGET_URL")


def update_XpEmployee(mainPostCompany_id, additionalPostCompany_id, secondmentCompany_id, self, data, backup_data=None):
    try:
        # update values for test cases
        data.mainPostCompany_id = mainPostCompany_id
        data.additionalPostCompany_id = additionalPostCompany_id
        data.secondmentCompany_id = secondmentCompany_id
        db.session.commit()

        # refresh the web page
        self.driver.refresh()
    except Exception as e:
        # roleback all values
        print(e)
        data.mainPostCompany_id = backup_data.mainPostCompany_id
        data.additionalPostCompany_id = backup_data.additionalPostCompany_id
        data.secondmentCompany_id = backup_data.secondmentCompany_id
        db.session.commit()


def update_UserRoles(role_id, data, backup_role_id=None):
    try:
        # update values for test cases
        data.role_id = role_id
        db.session.commit()
    except Exception as e:
        # roleback all values
        print(e)
        data.role_id = backup_role_id.mainPostCompany_id
        db.session.commit()

def wait_for_loading(driver, target_url, waiting_seconds):
    for _ in range(waiting_seconds):
        if driver.current_url == target_url:
            break
        sleep(1)
    else:
        raise Exception("Time limit exceeded")
    

def test_login_chrome():
    # Create a Chrome driver instance using the Service object
    driver = webdriver.Chrome(service=Service(executable_path="/path/to/chromedriver"))
    driver.get(url)
    
    driver.implicitly_wait(30)
    # textbox(id)
    driver.find_element(By.ID, "input28").send_keys(id)
    # checkbox(keep me signed in)
    driver.find_element(By.XPATH, "//*[@id='form20']/div[1]/div[3]/div[2]/div/span/div/label").click()
    # button(next)
    driver.find_element(By.CLASS_NAME, "button-primary").click()

    driver.implicitly_wait(30)
    # button()
    driver.find_element(By.XPATH, "//*[@id='form20']/div[2]/div/div[2]/div[2]/div[2]/a").click()

    # check okta login and current url(main page)
    # waiting for 3 minutes
    wait_for_loading(driver, url, 180)

    return driver