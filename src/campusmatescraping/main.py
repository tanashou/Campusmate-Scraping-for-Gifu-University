import campusmatescraping.scrape_events as scrape_events
import campusmatescraping.quickstart as quickstart
if __name__ == "__main__":
    driver = scrape_events.campusmate_login()
    # TODO: 日付指定か授業の予定がなくなるまでにしたい。数字の入力を無くしたい
    print("何週間分の予定を取得しますか？")
    try:
        NUM_OF_WEEKS = int(input(">"))
    except:
        print("数字を入力してください")
        exit()

    events = scrape_events.get_events(NUM_OF_WEEKS, driver)
    driver.quit()

    quickstart.add_events_to_calendar(events)
