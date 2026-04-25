import json
from datetime import date
from pathlib import Path

from user import User


class ReminderManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._users = {}
        return cls._instance

    def add_user(self, user):
        if user.username in self._users:
            raise ValueError("User already exists.")
        self._users[user.username] = user

    def remove_user(self, username):
        if username not in self._users:
            return False

        del self._users[username]
        return True

    def get_user(self, username):
        return self._users.get(username)

    def get_all_users(self):
        return list(self._users.values())

    def save_to_file(self, filename):
        data = {}

        for username, user in self._users.items():
            data[username] = user.to_dict()

        path = Path(filename)

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_file(self, filename):
        path = Path(filename)

        if not path.exists():
            self._users = {}
            return

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._users = {}

        for username, user_data in data.items():
            self._users[username] = User.from_dict(user_data)

    def send_today_notifications(self, sender, current_date=None):
        if current_date is None:
            current_date = date.today()

        for user in self._users.values():
            today_birthdays = user.reminder_book.get_today_birthdays(current_date)

            for entry in today_birthdays:
                sender.send(user, entry)

    def clear_all(self):
        self._users = {}
        
