import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from gifu_uni_scraper.event_info import EventInfo
from datetime import datetime
import time
import pyotp
from urllib.parse import urlparse, parse_qs

URL = "https://alss-portal.gifu-u.ac.jp/campusweb/top.do"
USERNAME = os.environ.get("TACT_USERNAME")
PASSWORD = os.environ.get("TACT_PASSWORD")
EMAIL_INPUT_BOX_ID = "i0116"
CONFIRM_BUTTON_ID = "idSIButton9"
PASSWORD_INPUT_BOX_ID = "i0118"
ONETIME_PASSWORD_INPUT_BOX_ID = "idTxtBx_SAOTCC_OTC"
VERIFY_BUTTON_ID = "idSubmit_SAOTCC_Continue"
ACCEPT_BUTTON_XPATH = '//input[@name="_eventId_proceed"]'


def wait_for_page_load(driver: webdriver.Chrome):
    return WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"  # type: ignore
    )


def get_otp() -> str:
    otp_uri = os.getenv("TACT_OTP_URI")

    if otp_uri:
        parsed_uri = urlparse(otp_uri)
        query_params = parse_qs(parsed_uri.query)

        if "secret" in query_params:
            secret_key = query_params["secret"][0]
            totp = pyotp.TOTP(secret_key)
            otp = totp.now()

            return otp
        else:
            raise ValueError(
                "ワンタイムパスワードを生成できませんでした。URIが正しいか確認してください。"
            )
    else:
        return input("ワンタイムパスワードを入力してください:\n>")


def transition_to_otp_input_window(driver) -> None:
    wait_for_page_load(driver)
    change_sign_in_mode_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "signInAnotherWay"))
    )
    change_sign_in_mode_button.click()

    wait_for_page_load(driver)
    use_verification_code_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-value="PhoneAppOTP"]'))
    )
    use_verification_code_button.click()


def login(headless):
    options = ChromeOptions()
    if headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    driver.get(URL)

    wait_for_page_load(driver)
    email_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, EMAIL_INPUT_BOX_ID))
    )
    email_input.send_keys(USERNAME)

    wait_for_page_load(driver)
    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, CONFIRM_BUTTON_ID))
    )
    next_button.click()

    wait_for_page_load(driver)
    password_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, PASSWORD_INPUT_BOX_ID))
    )
    password_input.send_keys(PASSWORD)
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, CONFIRM_BUTTON_ID))
    )
    sign_in_button.click()

    transition_to_otp_input_window(driver)

    wait_for_page_load(driver)
    otp_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, ONETIME_PASSWORD_INPUT_BOX_ID))
    )

    otp = get_otp()
    otp_input.send_keys(otp)

    wait_for_page_load(driver)
    verify_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, VERIFY_BUTTON_ID))
    )
    verify_button.click()

    wait_for_page_load(driver)
    stay_signed_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, CONFIRM_BUTTON_ID))
    )
    stay_signed_in_button.click()

    wait_for_page_load(driver)
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, ACCEPT_BUTTON_XPATH))
    )
    accept_button.click()

    wait_for_page_load(driver)

    return driver


def get_week_info(driver):
    day_elements = driver.find_elements(
        By.XPATH, '//th[contains(@class, "corner_1") or contains(@class, "corner_2")]'
    )
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
            event_text = detail.find_element(
                By.XPATH, './/span[contains(@class, "text")]'
            ).text.strip()
            period_text = detail.find_element(By.CLASS_NAME, "period").text.strip()
            daily_events.append((period_text, event_text))

        weekly_events.append(daily_events)
    return weekly_events


def get_weekly_events_with_date(driver):
    week_info = get_week_info(driver)
    weekly_events = get_weekly_events(driver)
    return list(zip(week_info, weekly_events))


def parse_events(events):
    result = []

    for datetime, daily_events in events:
        for period, event_text in daily_events:
            event = EventInfo(datetime, period, event_text)
            result.append(event)

    return result


def get_events_until(driver, month, day):
    result = []
    current_date = datetime.now()
    target_date = datetime(
        current_date.year
        + (
            month < current_date.month
            or (month == current_date.month and day < current_date.day)
        ),
        month,
        day,
    )

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    while True:
        time.sleep(1)  # Consider using WebDriverWait for a more efficient approach
        weekly_events = get_weekly_events_with_date(driver)

        for (event_month, event_day), daily_events in weekly_events:
            event_year = current_date.year + (
                event_month < current_date.month
                or (event_month == current_date.month and event_day < current_date.day)
            )
            event_datetime = datetime(event_year, event_month, event_day)

            if event_datetime > target_date:
                return parse_events(result)

            if daily_events:
                result.append((event_datetime, daily_events))

        next_week_button = driver.find_element(By.ID, "NextWeekButton")
        next_week_button.click()


if __name__ == "__main__":
    driver = login()
    events = get_events_until(driver, 4, 30)
    for event in events:
        print(event)
