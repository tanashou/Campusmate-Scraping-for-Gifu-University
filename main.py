import scrapeEvents
import quickstart

if __name__ == "__main__":
    NUM_OF_WEEKS = 20

    driver = scrapeEvents.campusmate_login()
    events_list = scrapeEvents.get_events(NUM_OF_WEEKS, driver)
    driver.quit()

    add_events_to_calendar(events_list)
