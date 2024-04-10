import os
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta, timezone

from webdriver_manager.chrome import ChromeDriverManager


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


def campusmate_login():
    URL = os.environ.get("CAMPUSMATE_URL")

    USERNAME = os.environ.get("THERS_USER")
    PASSWORD = os.environ.get("THERS_PASS")

    options = ChromeOptions()
    # options.add_argument("--headless") # ヘッドレスモードを有効化
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(URL)

    driver.implicitly_wait(50)

    # Locate the email input field and enter the email
    email_input = driver.find_element(By.ID, "i0116")
    email_input.send_keys(USERNAME)

    # Click the "Next" button
    next_button = driver.find_element(By.ID, "idSIButton9")
    next_button.click()

    # Wait for the password input field to appear
    sleep(2)

    password_input = driver.find_element(By.ID, "i0118")
    password_input.send_keys(PASSWORD)

    signin_button = driver.find_element(By.ID, "idSIButton9")
    signin_button.click()

    sleep(2)

    one_time_password_input =driver.find_element(By.ID, "idTxtBx_SAOTCC_OTC")
    one_time_password_input.send_keys(input("ワンタイムパスワードを入力してください\n>"))

    verify_button = driver.find_element(By.ID, "idSubmit_SAOTCC_Continue")
    verify_button.click()

    stay_signed_in_button = driver.find_element(By.ID, "idSIButton9")
    stay_signed_in_button.click()

    sleep(5)

    accept_button = driver.find_element(By.NAME, "_eventId_proceed")
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
            daily_events = driver.find_element(By.XPATH,
                f"/html/body/div[1]/div[2]/table/tbody/tr/td[1]/div[2]/form/div/div[1]/div[2]/table/tbody/tr[3]/td[{j}]"
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
