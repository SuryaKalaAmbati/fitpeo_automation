from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


def move_slider(driver, slider_thumb, target_value):
    slider = driver.find_element(By.XPATH,
                                 '//span[@class="MuiSlider-root MuiSlider-colorPrimary MuiSlider-sizeMedium css-duk49p"]')
    slider_width = slider.size['width']

    total_range = 2000  # Assuming the slider's range is 0 to 2000
    initial_value = int(slider_thumb.find_element(By.XPATH, './input').get_attribute('value'))

    # Calculate the percentage position
    initial_percentage = initial_value / total_range
    target_percentage = target_value / total_range
    offset_percentage = target_percentage - initial_percentage

    # Calculate the target offset in pixels
    target_offset = slider_width * offset_percentage

    # Perform the action chain to drag the slider
    actions = ActionChains(driver)
    actions.click_and_hold(slider_thumb).move_by_offset(target_offset, 0).release().perform()


try:
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()
    # Navigate to FitPeo Homepage
    driver.get('https://fitpeo.com')
    time.sleep(2)

    # Navigate to the Revenue Calculator Page
    revenue_calculator_link = driver.find_element(By.LINK_TEXT, 'Revenue Calculator')
    revenue_calculator_link.click()
    time.sleep(2)

    # Wait for the slider thumb to be visible
    slider_thumb = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located(
            (By.XPATH,
             '//span[@class="MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary css-sy3s50"]')
        )
    )

    # Move slider to 820
    move_slider(driver, slider_thumb, 820)

    # Wait for the slider to update
    time.sleep(2)

    # Verify the input value
    slider_input = driver.find_element(By.XPATH,
                                       '//span[@class="MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary MuiSlider-thumb MuiSlider-thumbSizeMedium MuiSlider-thumbColorPrimary css-sy3s50"]/input')
    current_value = int(slider_input.get_attribute('value'))
    print(f"Slider value after move: {current_value}")

    # Adjust the text field
    text_field = driver.find_element(By.XPATH, '//input[@id=":r0:"]')
    text_field.click()
    text_field.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, 5, 6, 0)

    # Wait for the value to be updated
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.XPATH, '//input[@id=":r0:"]'), '560')
    )

    assert text_field.get_attribute('value') == '560'
    print("Value set to 560")

    text_field.click()
    text_field.send_keys(Keys.BACKSPACE, Keys.BACKSPACE, Keys.BACKSPACE, 8, 2, 0)

    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element_value((By.XPATH, '//input[@id=":r0:"]'), '820')
    )

    assert text_field.get_attribute('value') == '820'
    print("Value set to 820")

    # Select CPT Codes
    cpt_codes = ['CPT-99091', 'CPT-99453', 'CPT-99454', 'CPT-99474']
    for code in cpt_codes:
        try:
            checkbox = driver.find_element(By.XPATH, f'//p[text()="{code}"]/../label/span/input')
            if not checkbox.is_selected():
                checkbox.click()
                print(f"Checkbox for {code} clicked successfully.")
            else:
                print(f"Checkbox for {code} is already selected.")
        except Exception as e:
            print(f"Error clicking checkbox for {code}: {e}")

    # Validate Total Recurring Reimbursement
    total_reimbursement = driver.find_element(By.XPATH,
                                              "//p[text()='Total Recurring Reimbursement for all Patients Per Month:']/p")
    assert total_reimbursement.text == '$110700'

    print("All test cases passed.")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
