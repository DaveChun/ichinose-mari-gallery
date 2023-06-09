import os
import sys
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from common import common_for_test_automation as common
from copy import deepcopy
# Absolute env path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(ROOT_DIR, 'app/.env'))
sys.path.append(os.path.dirname(ROOT_DIR))

from app import db
from app.models import XpEmployee, UserRoles

top_url = os.environ.get("TARGET_URL")
id = os.environ.get("ID_FOR_TESTING") + "@rakuten.com"


'''
Common methods

'''
def test_login_no_01_to_12(index, role_id, mainPostCompany_id, additionalPostCompany_id, secondmentCompany_id, self, data, backup_data):
    common.update_XpEmployee(mainPostCompany_id, additionalPostCompany_id, secondmentCompany_id, self, data, backup_data)
    # Login_TC_092 to 096 / Login_TC_099 / Login_TC_100 
    if index == 1 or (index in [2, 3, 4, 5, 8] and role_id < 4):
        common.wait_for_loading(self.driver, top_url, 30)
        self.assertTrue(self.driver.current_url == top_url)

    # Login_TC_112 / Login_TC_113
    elif index in [11, 12]:
        tmp_url = top_url+'sign-in'
        common.wait_for_loading(self.driver, tmp_url, 30)
        self.assertTrue(self.driver.current_url == tmp_url)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, "ant-alert-message"), 'No Permission')
    
    # revert this code if all test cases covered.
    # else:
    #     raise Exception("Not covered all test cases")
    common.update_XpEmployee('1', '1', '1', self, data, backup_data)


'''
Test cases

'''
def test_user_role(self):
    self.driver.get(top_url)
    # Check if current url is the top page
    self.assertTrue(self.driver.current_url == top_url)

    # get/backup current values 
    user_info = XpEmployee.query.filter(XpEmployee.primaryEmail == id).first()
    backup_data = deepcopy(user_info)
    fixed_params = {
        'self': self,
        'data': user_info,
        'backup_data': backup_data
    }

    # get/backup current values
    user_role = UserRoles.query.filter(UserRoles.user_id == user_info.id).first()
    backup_user_role = deepcopy(user_role)

    # test not manager and manager roles
    roles = [1, 4]
    # test cases
    test_cases = {              # Not Manager cases  Manager cases
        1 : ['1', '1', '1'],    # Login_TC_092 O     Login_TC_100 O
        2 : ['1', '1', '2'],    # Login_TC_093 O     Login_TC_101 X
        3 : ['1', '2', '1'],    # Login_TC_094 O     Login_TC_102 X
        4 : ['1', None, '1'],   # Login_TC_095 O     Login_TC_103 X
        5 : ['2', '1', '1'],    # Login_TC_096 O     Login_TC_104 X
        6 : ['2', '1', '2'],    # Login_TC_097 X     Login_TC_105 X
        7 : ['2', '2', '1'],    # Login_TC_098 X     Login_TC_106 X
        8 : ['2', None, '1'],   # Login_TC_099 O     Login_TC_107 X
        9 : ['1', '2', '2'],    # Login_TC_108 X     Login_TC_110 X
        10 : ['1', '2', None],  # Login_TC_109 X     Login_TC_111 X
        11 : ['2', '2', '2'],   # Login_TC_112 O     Login_TC_112 O (The case is same as Non-Manager case)
        12 : ['2', None, '2'],  # Login_TC_113 O     Login_TC_113 O (The case is same as Non-Manager case)
    }
    for role in roles:
        # set role
        common.update_UserRoles(role, user_role, backup_user_role)
        # test login test cases
        for index, case in test_cases.items():
            test_login_no_01_to_12(index, role, case[0], case[1], case[2], **fixed_params)

    # revert all values
    common.update_XpEmployee(backup_data.mainPostCompany_id, backup_data.additionalPostCompany_id, backup_data.secondmentCompany_id, **fixed_params)
    common.update_UserRoles(backup_user_role.role_id, user_role, backup_user_role)
    
