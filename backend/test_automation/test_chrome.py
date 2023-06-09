
from selenium.webdriver.common.by import By
import unittest
from testcases import test_top, test_login, test_contractor
from test_automation.common import common_for_test_automation as common
import os
from dotenv import load_dotenv
from app.models import XpEmployee, UserRoles

# Absolute env path
# ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# load_dotenv(os.path.join(ROOT_DIR, 'app/.env'))

top_url = os.environ.get("TARGET_URL")
id = os.environ.get("ID_FOR_TESTING") + "@rakuten.com"


'''
Common methods

'''
def set_default(cls):
    user_info = XpEmployee.query.filter(XpEmployee.primaryEmail == id).first()
    user_role = UserRoles.query.filter(UserRoles.user_id == user_info.id).first()
    common.update_XpEmployee('1', '1', '1', cls, user_info)
    common.update_UserRoles(4, cls, user_role)


'''
Class for testing

'''
class TestChrome(unittest.TestCase):
    

    '''
    SetUp/tearDown instances or variables in Class level

    '''
    @classmethod
    def setUpClass(cls):
        # Open the driver
        cls.driver = common.test_login_chrome()
        set_default(cls)

    
    @classmethod
    def tearDownClass(cls):
        set_default(cls)
        # Close the driver
        cls.driver.quit()


    '''
    SetUp/tearDown instances or variables in Method level 
    
    
    '''
    def setUp(self):
        # Move to the top page
        self.driver.get(top_url)


    def tearDown(self):
        pass
    


    '''
    Test the user role
    
    '''
    def test_login(self):
        # Case: Check user rolls
        test_login.test_user_role(self)
        
    
    '''
    Test the top page
    
    '''
    def test_top_page(self):
        # Case
        test_top.test_aaaa(self)


    # '''
    # Test for contracrtor page
    
    # '''
    # def test_contractor_page(self):
    #     # Case 1
    #     test_contractor.test_contractor_aaa(self)


if __name__ == '__main__':
    unittest.main()