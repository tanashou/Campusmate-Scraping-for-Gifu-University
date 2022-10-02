import scrapeEvents
import quickstart

if __name__ == "__main__":
    driver = scrapeEvents.campusmate_login()

    print("何週間分の予定を取得しますか？")
    try:
        NUM_OF_WEEKS = int(input(">"))
    except:
        print("数字を入力してください")
        exit()

    events = scrapeEvents.get_events(NUM_OF_WEEKS, driver)
    driver.quit()

    quickstart.add_events_to_calendar(events)
