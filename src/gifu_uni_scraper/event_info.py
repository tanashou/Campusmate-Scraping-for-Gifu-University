from datetime import datetime


class EventInfo:
    PERIOD_TIMES = {
        "１時限": {"start": (8, 45), "end": (10, 15)},
        "２時限": {"start": (10, 30), "end": (12, 0)},
        "３時限": {"start": (13, 0), "end": (14, 30)},
        "４時限": {"start": (14, 45), "end": (16, 15)},
        "５時限": {"start": (16, 30), "end": (18, 0)},
    }

    def __init__(self, datetime: datetime, period, event_text):
        self.start_date_time = datetime
        self.end_date_time = datetime
        self.event_text = event_text
        self.is_one_day_event = True

        period_time = self.PERIOD_TIMES.get(period)
        if period_time:
            self.is_one_day_event = False
            start_hour, start_minute = period_time["start"]
            end_hour, end_minute = period_time["end"]

            self.start_date_time = self.start_date_time.replace(hour=start_hour, minute=start_minute).isoformat()
            self.end_date_time = self.end_date_time.replace(hour=end_hour, minute=end_minute).isoformat()

    def __str__(self) -> str:
        return f"{self.start_date_time} - {self.end_date_time}: {self.event_text}"
