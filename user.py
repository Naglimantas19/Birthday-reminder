from reminder_book import ReminderBook


class User:
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self._reminder_book = ReminderBook()

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")
        self._username = value.strip()

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if "@" not in value or "." not in value:
            raise ValueError("Email is not valid.")
        self._email = value.strip()

    @property
    def reminder_book(self):
        return self._reminder_book

    def add_birthday(self, person_name, birthday):
        self._reminder_book.add_birthday(person_name, birthday)

    def remove_birthday(self, person_name):
        return self._reminder_book.remove_birthday(person_name)

    def get_upcoming_birthdays(self, current_date, days_ahead=7):
        return self._reminder_book.get_upcoming_birthdays(current_date, days_ahead)

    def to_dict(self):
        return {
            "username": self._username,
            "email": self._email,
            "birthdays": self._reminder_book.to_dict()
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["username"], data["email"])
        user.reminder_book.load_from_dict(data.get("birthdays", []))
        return user