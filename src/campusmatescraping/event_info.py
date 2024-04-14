class EventInfo:
    # Define a class-level dictionary for period time mappings
    PERIOD_TIMES = {
        "１時限": {"start": (8, 45), "end": (10, 15)},
        "２時限": {"start": (10, 30), "end": (12, 0)},
        "３時限": {"start": (13, 0), "end": (14, 30)},
        "４時限": {"start": (14, 45), "end": (16, 15)},
        "５時限": {"start": (16, 30), "end": (18, 0)},
    }

    def __init__(self, string, date):
        lines = string.splitlines()  # Store split lines to avoid multiple splits
        if "時限" in string:
            self.name = lines[1]
            self.one_day_event = False

            # Get the start and end times from the dictionary
            period = lines[0]
            if period in self.PERIOD_TIMES:
                start_hour, start_minute = self.PERIOD_TIMES[period]["start"]
                end_hour, end_minute = self.PERIOD_TIMES[period]["end"]

                self.start_date_time = date.replace(hour=start_hour, minute=start_minute).isoformat()
                self.end_date_time = date.replace(hour=end_hour, minute=end_minute).isoformat()

        else:
            self.date = date.isoformat().split("T")[0]
            self.name = string
            self.one_day_event = True
