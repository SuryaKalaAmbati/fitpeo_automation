from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

try:
    # Initialize WebDriver
    driver = webdriver.Chrome()

    # Navigate to FitPeo Homepage
    driver.get('https://fitpeo.com')
    time.sleep(2)

    # Navigate to the Revenue Calculator Page
    revenue_calculator_link = driver.find_element(By.LINK_TEXT, 'Revenue Calculator')
    revenue_calculator_link.click()
    time.sleep(2)

    # Scroll Down to the Slider section
    slider = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'slider'))  # Assuming the slider has an ID 'slider'
    )
    driver.execute_script("arguments[0].scrollIntoView(true);", slider)

    # Adjust the Slider to 820
    ActionChains(driver).drag_and_drop_by_offset(slider, 820, 0).perform()

    # Update the Text Field to 560
    text_field = driver.find_element(By.ID, 'text_field')  # Assuming the text field has an ID 'text_field'
    text_field.click()
    text_field.clear()
    text_field.send_keys('560')
    text_field.send_keys(Keys.RETURN)

    # Validate the Slider Value
    slider_value = driver.find_element(By.ID,
                                       'slider_value')  # Assuming the slider value can be checked via ID 'slider_value'
    assert slider_value.get_attribute('value') == '560'

    # Select CPT Codes
    cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']
    for code in cpt_codes:
        checkbox = driver.find_element(By.ID, code)
        if not checkbox.is_selected():
            checkbox.click()

    # Validate Total Recurring Reimbursement and Exception Handling and Finalization:
    total_reimbursement = driver.find_element(By.ID,
                                              'total_reimbursement')  # Assuming the total reimbursement has an ID 'total_reimbursement'
    assert total_reimbursement.text == '$110700'

    print("All test cases passed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Close the browser
    driver.quit()
