import os
import sys
from dotenv import load_dotenv
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep

# Absolute env path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(ROOT_DIR, 'app/.env'))
sys.path.append(os.path.dirname(ROOT_DIR))

top_url = os.environ.get("TARGET_URL")


def test_contractor_aaa(self):
    self.driver.get(top_url)
    self.assertTrue(self.driver.current_url == top_url)