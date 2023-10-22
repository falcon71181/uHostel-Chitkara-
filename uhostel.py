import json
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

def load_config(config_file_path):
    try:
        with open(config_file_path, "r") as config_file:
            config_data = json.load(config_file)
        return config_data
    except Exception as e:
        print(f"Failed to load configuration: {e}")
        return None

def login(driver, username, password):
    try:
        driver.get("https://uhostel.chitkara.edu.in/")
        assert "Hostel" in driver.title
        rollno = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        rollno.clear()
        rollno.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        rollno.send_keys(Keys.RETURN)
        assert "Current password" in driver.page_source
    except Exception as e:
        print(f"Failed to log in: {e}")

def fill_gate_pass(driver, out_time, in_time, leaving_reason, desired_day, desired_month, desired_year):
    try:
        gatepass_url = "https://uhostel.chitkara.edu.in/Gatepass"
        driver.get(gatepass_url)
        driver.find_element(By.XPATH, '//*[@id="addbtn"]').click()

        timeout = driver.find_element(By.NAME, "checkoutTime")
        timein = driver.find_element(By.NAME, "checkinTime")
        reason = driver.find_element(By.NAME, "reason")
        timeout.clear()
        timeout.send_keys(out_time)
        timein.clear()
        timein.send_keys(in_time)
        reason.clear()
        reason.send_keys(leaving_reason)

        leaving_date = driver.find_element(By.NAME, "dateCheckOut").click()

        dropdown_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-year")
        select = Select(dropdown_element)
        select.select_by_value(desired_year)

        dropdown_element = driver.find_element(By.CLASS_NAME, "ui-datepicker-month")
        select = Select(dropdown_element)
        select.select_by_visible_text(desired_month)

        day_element = driver.find_element(By.LINK_TEXT, desired_day)
        day_element.click()

        submit_button = driver.find_element(By.XPATH, '//*[@id="saveBtn"]/span')
        submit_button.click()
    except Exception as e:
        print(f"Failed to fill out gate pass: {e}")

def main():
    config_file_path = "data.config"
    config_data = load_config(config_file_path)
    
    if config_data:
        try:
            driver = webdriver.Chrome()
            login(driver, config_data["username"], config_data["pass_word"])
            fill_gate_pass(driver, config_data["out_time"], config_data["in_time"], config_data["leaving_reason"],
                           config_data["desired_day"], config_data["desired_month"], config_data["desired_year"])
            alert = Alert(driver)
            alert.accept()
            time.sleep(3)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()

