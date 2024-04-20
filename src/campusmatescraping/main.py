from campusmatescraping import scrape_events, quickstart
from datetime import datetime


def get_user_input_date():
    while True:
        try:
            month, day = map(int, input("いつまでの予定を取得しますか？日付を入力してください (M/D):\n>").split("/"))

            current_year = datetime.now().year
            current_month = datetime.now().month
            current_day = datetime.now().day

            if (month < current_month) or (month == current_month and day < current_day):
                current_year += 1

            input_date = datetime(current_year, month, day)
            return input_date
        except ValueError as e:
            print("有効な日付を入力してください", e)


if __name__ == "__main__":
    headless = input("ヘッドレスモードで実行しますか？(y/n)\n>").lower() == "y"
    driver = scrape_events.login(headless)
    inputted_date = get_user_input_date()
    events = scrape_events.get_events_until(driver, inputted_date.month, inputted_date.day)
    driver.quit()

    quickstart.add_events_to_calendar(events)
