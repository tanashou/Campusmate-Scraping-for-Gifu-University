import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from campusmatescraping.event_info import EventInfo
from datetime import datetime
import time

URL = "https://alss-portal.gifu-u.ac.jp/campusweb/top.do"
USERNAME = os.environ.get("GIFU_SCRAPER_USERNAME")
PASSWORD = os.environ.get("GIFU_SCRAPER_PASSWORD")
EMAIL_INPUT_BOX_ID = "i0116"
CONFIRM_BUTTON_ID = "idSIButton9"
PASSWORD_INPUT_BOX_ID = "i0118"
ONETIME_PASSWORD_INPUT_BOX_ID = "idTxtBx_SAOTCC_OTC"
VERIFY_BUTTON_ID = "idSubmit_SAOTCC_Continue"
ACCEPT_BUTTON_XPATH = '//input[@name="_eventId_proceed"]'


def wait_for_element(driver, timeout, locator):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def login():
    options = ChromeOptions()
    # Uncomment the line below to enable headless mode
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    email_input = wait_for_element(driver, 10, (By.ID, EMAIL_INPUT_BOX_ID))
    email_input.send_keys(USERNAME)

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    next_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    next_button.click()

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    password_input = wait_for_element(driver, 10, (By.ID, PASSWORD_INPUT_BOX_ID))
    password_input.send_keys(PASSWORD)
    sign_in_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    sign_in_button.click()

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    one_time_password_input = wait_for_element(driver, 10, (By.ID, ONETIME_PASSWORD_INPUT_BOX_ID))
    one_time_password_input.send_keys(input("Please enter the one-time password:\n>"))

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    verify_button = wait_for_element(driver, 10, (By.ID, VERIFY_BUTTON_ID))
    verify_button.click()

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    stay_signed_in_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    stay_signed_in_button.click()

    WebDriverWait(driver, 10).until(lambda d: d.execute_script("return document.readyState") == "complete")
    accept_button = wait_for_element(driver, 10, (By.XPATH, ACCEPT_BUTTON_XPATH))
    accept_button.click()

    return driver


def get_week_info(driver):
    day_elements = driver.find_elements(By.XPATH, '//th[contains(@class, "corner_1") or contains(@class, "corner_2")]')
    result = []

    for day_element in day_elements:
        date_element = day_element.find_element(By.XPATH, ".//a")
        date_string = date_element.text

        match = re.search(r"(\d+)/\s*(\d+)", date_string)
        month = int(match.group(1))
        day = int(match.group(2))
        result.append((month, day))

    return result


def get_weekly_events(driver):
    td_elements = driver.find_elements(By.XPATH, '//td[contains(@class, "in_line_y")]')
    weekly_events = []

    for td in td_elements:
        details = td.find_elements(By.CLASS_NAME, "details")
        daily_events = []

        for detail in details:
            event_text = detail.find_element(By.XPATH, './/span[contains(@class, "text")]').text.strip()
            period_text = detail.find_element(By.CLASS_NAME, "period").text.strip()
            daily_events.append((period_text, event_text))

        weekly_events.append(daily_events)
    return weekly_events


def get_weekly_events_with_date(driver):
    week_info = get_week_info(driver)
    weekly_events = get_weekly_events(driver)
    # TODO: ここでクラスに変換して返す
    return list(zip(week_info, weekly_events))


def get_events_until(driver, month, day):  # 一年以上先のイベントは取得しない
    result = []

    current_year = datetime.now().year
    target_date = datetime(current_year, month, day)

    while True:
        time.sleep(1) # 要素がロードされるまで待つ。他にいい方法があれば変更したい
        weekly_events = get_weekly_events_with_date(driver)

        for (event_month, event_day), daily_events in weekly_events:
            event_date = datetime(current_year, event_month, event_day)
            if event_date > target_date:
                return result

            if daily_events:
                result.append((event_month, event_day, daily_events))

        next_week_button = driver.find_element(By.ID, "NextWeekButton")
        next_week_button.click()


if __name__ == "__main__":
    driver = login()
    print(get_events_until(driver, 6, 30))
