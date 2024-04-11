import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from time import sleep
from datetime import datetime, timedelta, timezone
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://alss-portal.gifu-u.ac.jp/campusweb/top.do"
USERNAME = os.environ.get("GIFU_SCRAPER_USERNAME")
PASSWORD = os.environ.get("GIFU_SCRAPER_PASSWORD")
EMAIL_INPUT_BOX_ID = "i0116"
CONFIRM_BUTTON_ID = "idSIButton9"
PASSWORD_INPUT_BOX_ID = "i0118"
ONETIME_PASSWORD_INPUT_BOX_ID = "idTxtBx_SAOTCC_OTC"
VERIFY_BUTTON_ID = "idSubmit_SAOTCC_Continue"
ACCEPT_BUTTON_XPATH = '//input[@name="_eventId_proceed"]'


class EventInfo:
    def __init__(self, string, date):
        if "時限" in string:
            self.name = string.splitlines()[1]
            self.one_day_event = False

            if string.splitlines()[0] == "１時限":
                self.start_date_time = date.replace(hour=8, minute=45).isoformat()
                self.end_date_time = date.replace(hour=10, minute=15).isoformat()
            elif string.splitlines()[0] == "２時限":
                self.start_date_time = date.replace(hour=10, minute=30).isoformat()
                self.end_date_time = date.replace(hour=12, minute=00).isoformat()
            elif string.splitlines()[0] == "３時限":
                self.start_date_time = date.replace(hour=13, minute=00).isoformat()
                self.end_date_time = date.replace(hour=14, minute=30).isoformat()
            elif string.splitlines()[0] == "４時限":
                self.start_date_time = date.replace(hour=14, minute=45).isoformat()
                self.end_date_time = date.replace(hour=16, minute=15).isoformat()
            elif string.splitlines()[0] == "５時限":
                self.start_date_time = date.replace(hour=16, minute=30).isoformat()
                self.end_date_time = date.replace(hour=18, minute=00).isoformat()

        else:
            self.date = date.isoformat().split("T")[0]
            self.name = string
            self.one_day_event = True


def wait_for_element(driver, timeout, locator):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))


def login():
    options = ChromeOptions()
    # Uncomment the line below to enable headless mode
    # options.add_argument("--headless")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(URL)

    email_input = wait_for_element(driver, 10, (By.ID, EMAIL_INPUT_BOX_ID))
    email_input.send_keys(USERNAME)

    next_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    next_button.click()

    password_input = wait_for_element(driver, 10, (By.ID, PASSWORD_INPUT_BOX_ID))
    password_input.send_keys(PASSWORD)

    sign_in_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    sign_in_button.click()

    one_time_password_input = wait_for_element(driver, 10, (By.ID, ONETIME_PASSWORD_INPUT_BOX_ID))
    one_time_password_input.send_keys(input("Please enter the one-time password:\n>"))

    verify_button = wait_for_element(driver, 10, (By.ID, VERIFY_BUTTON_ID))
    verify_button.click()

    stay_signed_in_button = wait_for_element(driver, 10, (By.ID, CONFIRM_BUTTON_ID))
    stay_signed_in_button.click()

    accept_button = wait_for_element(driver, 10, (By.XPATH, ACCEPT_BUTTON_XPATH))
    accept_button.click()

    return driver


def get_events(num_of_weeks, driver):
    tokyo_tz = timezone(timedelta(hours=9))
    today = datetime.now(tokyo_tz)  # 取得する授業イベントの始まり
    day_offset = 0
    events = []

    # 何周分処理を行うか
    for _ in range(num_of_weeks):
        next_week_button = driver.find_element(By.ID, "NextWeekButton")

        # 1週間分の処理(jはxpathより)
        for j in range(2, 9):
            event_date = today + timedelta(days=day_offset)
            day_offset += 1
            daily_events = driver.find_element(
                By.XPATH,
                f"/html/body/div[1]/div[2]/table/tbody/tr/td[1]/div[2]/form/div/div[1]/div[2]/table/tbody/tr[3]/td[{j}]",
            )

            if daily_events.text == "":  # 取得した日が空欄の場合
                continue

            course_detail = daily_events.find_elements(By.CLASS_NAME, "details")

            # 1日分の処理
            for detail in course_detail:
                string = detail.text
                event = EventInfo(string, event_date)
                events.append(event)

        next_week_button.click()
        sleep(2)

    return events


if __name__ == "__main__":
    driver = login()
