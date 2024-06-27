import json
import os

import selenium.webdriver as webdriver
from dotenv import load_dotenv
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

load_dotenv()
BROWSERSTACK_UI_USER = os.environ.get("BROWSERSTACK_UI_USER") or "BROWSERSTACK_UI_USER"
BROWSERSTACK_UI_PASSWORD = os.environ.get("BROWSERSTACK_UI_PASSWORD") or "BROWSERSTACK_UI_PASSWORD"


def run_clean():
    try:
        driver = webdriver.Chrome()
        driver.maximize_window()

        driver.get("https://www.browserstack.com/")

        # Attempt sign in
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.LINK_TEXT, "Sign in"))).click()
        except TimeoutException:

            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "primary-menu-toggle"))).click()

                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign in"))).click()
            except TimeoutException:
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                        "Failed to sign in") + '}}')
                assert False, "Failed to sign in"

        email_input = driver.find_element(by=By.ID, value="user_email_login")
        email_input.send_keys(BROWSERSTACK_UI_USER)

        password_input = driver.find_element(by=By.ID, value="user_password")
        password_input.send_keys(BROWSERSTACK_UI_PASSWORD)

        driver.find_element(by=By.ID, value="user_submit").click()

        # Attempt to click on the "Invite team" link
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
                (By.ID, "invite-link"))).click()
        except TimeoutException:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "primary-menu-toggle"))).click()

                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "invite-link"))).click()
            except TimeoutException:
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                        "Failed to get to invite link page") + '}}')
                assert False, "Failed to get to invite link page"

        # Attempt to copy link text
        try:
            the_link = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[@class='manage-users__invite-copyLink-text']"))).text
        except TimeoutException:
            driver.execute_script(
                'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                    "Failed to find and copy the invite link") + '}}')
            assert False, "Failed to find and copy the invite link"

        # Attempt to sign out
        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "account-menu-toggle"))).click()

            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "sign_out_link"))).click()
        except TimeoutException:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "primary-menu-toggle"))).click()

                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.LINK_TEXT, "Sign out"))).click()
            except TimeoutException:
                driver.execute_script(
                    'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                        "Failed to sign out") + '}}')
                assert False, "Failed to sign out"

    # Catch any exceptions not encountered so far
    except NoSuchElementException as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                message) + '}}')
    except Exception as err:
        message = "Exception: " + str(err.__class__) + str(err.msg)
        driver.execute_script(
            'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"failed", "reason": ' + json.dumps(
                message) + '}}')

    driver.execute_script(
        'browserstack_executor: {"action": "setSessionStatus", "arguments": {"status":"passed", "reason": ' + json.dumps(
            f"test successful!  Login, url validated {the_link}, and logged out") + '}}')
    driver.quit()


run_clean()
