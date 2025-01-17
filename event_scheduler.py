import json
import os

class EventScheduler:
    def __init__(self):
        self.scheduled_events = {}
        self.load()

    def schedule_event(self, event, time):
        self.scheduled_events[time] = event
        print(f"Scheduling event {event} at time {time}")
        self.save()

    def save(self):
        with open("events.json", "w") as f:
            json.dump(self.scheduled_events, f, indent=4)

    def load(self):
        if os.path.exists("events.json"):
            with open("events.json", "r") as f:
                self.scheduled_events = json.load(f)