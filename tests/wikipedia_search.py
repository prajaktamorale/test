import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Configure BrowserStack options
options = ChromeOptions()
options.set_capability('sessionName', 'Wikipedia Search Test')

# Initialize WebDriver
driver = webdriver.Chrome(options=options)

try:
   # Open Wikipedia
   driver.get('https://www.wikipedia.org/')
   
   # Wait until the search bar is visible
   search_box = WebDriverWait(driver, 10).until(
       EC.visibility_of_element_located((By.NAME, 'search'))
   )
   
   # Type 'Mumbai' in the search bar and submit
   search_box.send_keys('Mumbai')
   search_box.submit()
   
   # Wait for the Mumbai Wikipedia page to load
   WebDriverWait(driver, 10).until(EC.title_contains('Mumbai'))
   
   # Get the title of the Wikipedia page
   page_title = driver.title
   
   # Verify that the search was successful
   if 'Mumbai' in page_title:
       driver.execute_script(
           'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": "Successfully opened Mumbai Wikipedia page!"}}'
       )
   else:
       driver.execute_script(
           'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": "Mumbai Wikipedia page did not open!"}}'
       )
except NoSuchElementException as err:
   message = 'Exception: ' + str(err.__class__) + str(err.msg)
   driver.execute_script(
       'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}'
   )
except Exception as err:
   message = 'Exception: ' + str(err.__class__) + str(err.msg)
   driver.execute_script(
       'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(message) + '}}'
   )
finally:
   # Stop the driver
   driver.quit()

executor_object = {
    'action': 'setSessionName',
    'arguments': {
        'name': "<test-name>"
    }
}
browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
driver.execute_script(browserstack_executor)

executor_object = {
    'action': 'setSessionStatus',
    'arguments': {
        'status': "<passed/failed>",
        'reason': "<reason>"
    }
}
browserstack_executor = 'browserstack_executor: {}'.format(json.dumps(executor_object))
driver.execute_script(browserstack_executor)