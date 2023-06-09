
import pytest
import os

# Get the directory of the test files
dir_path = os.path.dirname(os.path.realpath(__file__))
selenium_files = [f for f in os.listdir(dir_path) if f.endswith('.py') and f.startswith('test_')]

# Import all the test files
for file in selenium_files:
    module_name = file.replace('.py', '')
    exec(f"from {module_name} import *")
    


# Define a test case that runs all the tests in the test files
def test_all():
    for _ in selenium_files:
        exec(f"pytest.main(['-q', os.path.join(dir_path, file)])")


if __name__ == '__main__':
    # Execute all test files
    test_all()