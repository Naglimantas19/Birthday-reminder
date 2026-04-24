from birthday_entry import BirthdayEntry


class ReminderBook:
    def __init__(self):
        self._birthdays = []

    @property
    def birthdays(self):
        return self._birthdays

    def add_birthday(self, person_name, birthday):
        if self.find_birthday(person_name) is not None:
            raise ValueError("Birthday for this person already exists.")

        entry = BirthdayEntry(person_name, birthday)
        self._birthdays.append(entry)

    def remove_birthday(self, person_name):
        entry = self.find_birthday(person_name)

        if entry is None:
            return False

        self._birthdays.remove(entry)
        return True

    def find_birthday(self, person_name):
        for entry in self._birthdays:
            if entry.person_name.lower() == person_name.lower():
                return entry
        return None

    def get_upcoming_birthdays(self, current_date, days_ahead=7):
        upcoming = []

        for entry in self._birthdays:
            if entry.is_upcoming(current_date, days_ahead):
                upcoming.append(entry)

        return sorted(
            upcoming,
            key=lambda entry: entry.days_until_birthday(current_date)
        )

    def get_today_birthdays(self, current_date):
        return [entry for entry in self._birthdays if entry.is_today(current_date)]

    def to_dict(self):
        return [entry.to_dict() for entry in self._birthdays]

    def load_from_dict(self, data):
        self._birthdays = [BirthdayEntry.from_dict(item) for item in data]