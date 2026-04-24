from datetime import date, datetime


class BirthdayEntry:
    def __init__(self, person_name, birthday):
        self.person_name = person_name
        self.birthday = birthday

    @property
    def person_name(self):
        return self._person_name

    @person_name.setter
    def person_name(self, value):
        if not value or not value.strip():
            raise ValueError("Person name cannot be empty.")
        self._person_name = value.strip()

    @property
    def birthday(self):
        return self._birthday

    @birthday.setter
    def birthday(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Birthday must be in YYYY-MM-DD format.")
        self._birthday = value

    def get_date(self):
        return datetime.strptime(self._birthday, "%Y-%m-%d").date()

    def is_today(self, current_date):
        birthday_date = self.get_date()
        return birthday_date.month == current_date.month and birthday_date.day == current_date.day

    def days_until_birthday(self, current_date):
        birthday_date = self.get_date()
        next_birthday = date(current_date.year, birthday_date.month, birthday_date.day)

        if next_birthday < current_date:
            next_birthday = date(current_date.year + 1, birthday_date.month, birthday_date.day)

        return (next_birthday - current_date).days

    def is_upcoming(self, current_date, days_ahead=7):
        days_left = self.days_until_birthday(current_date)
        return 0 <= days_left <= days_ahead

    def to_dict(self):
        return {
            "person_name": self._person_name,
            "birthday": self._birthday
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["person_name"], data["birthday"])