from campusmatescraping.event_info import EventInfo

class DailyEvents:
    def __init__(self, date):
        self.date = date
        self.events = []

    def add_event(self, event):
        self.events.append(event)

    def add_events(self, events):
        self.events.extend(events)