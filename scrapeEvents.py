import os
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from datetime import datetime, timedelta, timezone

from webdriver_manager.chrome import ChromeDriverManager


class EventInfoClass:
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
    URL = "https://alss-portal.gifu-u.ac.jp/"

    USERNAME = os.environ.get("UNI_USER")
    PASSWORD = os.environ.get("UNI_PASS")

    options = ChromeOptions()
    options.add_argument("--headless") # ヘッドレスモードを有効化
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

    driver.get(URL)

    driver.implicitly_wait(20)

    elem_username = driver.find_element_by_id("username_input")
    elem_password = driver.find_element_by_id("password_input")
    elem_login_button = driver.find_element_by_id("login_button")

    elem_username.send_keys(USERNAME)
    elem_password.send_keys(PASSWORD)
    elem_login_button.click()

    driver.implicitly_wait(20)

    try:
        elem_submit_button = driver.find_element_by_xpath(
            '//*[@id="t01"]/tbody/tr[2]/td/input'
        )
        elem_submit_button.click()

        driver.implicitly_wait(20)

        elem_otp_input = driver.find_element_by_id("password_input")
        elem_otp_submit_button = driver.find_element_by_id("login_button")

        print("ワンタイムパスワードを入力してください")
        otp = input(">")

        elem_otp_input.send_keys(otp)
        elem_otp_submit_button.click()

    except:
        print("ワンタイムパスワードは不要です")

    sleep(5)

    return driver


def get_events(num_of_weeks, driver):
    tokyo_tz = timezone(timedelta(hours=9))
    today = datetime.now(tokyo_tz)  # 取得する授業イベントの始まり
    day_offset = 0
    events_list = []

    # 何周分処理を行うか
    for _ in range(num_of_weeks):
        next_week_button = driver.find_element_by_id("NextWeekButton")

        # 1週間分の処理(jはxpathより)
        for j in range(2, 9):
            event_date = today + timedelta(days=day_offset)
            day_offset += 1
            daily_events = driver.find_element_by_xpath(
                f"/html/body/div[1]/div[2]/table/tbody/tr/td[1]/div[2]/form/div/div[1]/div[2]/table/tbody/tr[3]/td[{j}]"
            )

            if daily_events.text == "":  # 取得した日が空欄の場合
                continue

            course_detail = daily_events.find_elements(By.CLASS_NAME, "details")

            # 1日分の処理
            for detail in course_detail:
                string = detail.text
                tmp = EventInfoClass(string, event_date)
                events_list.append(tmp)

        next_week_button.click()
        sleep(2)

    return events_list


if __name__ == "__main__":
    driver = campusmate_login()
    events_list = get_events(5, driver)
    driver.quit()
