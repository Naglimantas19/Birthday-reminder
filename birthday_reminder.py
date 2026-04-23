from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
import json
from pathlib import Path
from typing import Any


class BirthdayEntry:
    def __init__(self, person_name: str, birthday: str):
        self.person_name = person_name
        self.birthday = birthday

    @property
    def person_name(self) -> str:
        return self._person_name

    @person_name.setter
    def person_name(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Person name cannot be empty.")
        self._person_name = value.strip()

    @property
    def birthday(self) -> str:
        return self._birthday

    @birthday.setter
    def birthday(self, value: str) -> None:
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError as error:
            raise ValueError("Birthday must be in YYYY-MM-DD format.") from error
        self._birthday = value

    def get_date(self) -> date:
        return datetime.strptime(self._birthday, "%Y-%m-%d").date()

    def is_today(self, current_date: date) -> bool:
        birthday_date = self.get_date()
        return (
            birthday_date.month == current_date.month
            and birthday_date.day == current_date.day
        )

    def days_until_birthday(self, current_date: date) -> int:
        birthday_date = self.get_date()
        next_birthday = date(
            current_date.year,
            birthday_date.month,
            birthday_date.day,
        )

        if next_birthday < current_date:
            next_birthday = date(
                current_date.year + 1,
                birthday_date.month,
                birthday_date.day,
            )

        return (next_birthday - current_date).days

    def is_upcoming(self, current_date: date, days_ahead: int = 7) -> bool:
        days_left = self.days_until_birthday(current_date)
        return 0 <= days_left <= days_ahead

    def to_dict(self) -> dict[str, Any]:
        return {
            "person_name": self._person_name,
            "birthday": self._birthday,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BirthdayEntry":
        return cls(data["person_name"], data["birthday"])


class ReminderBook:
    def __init__(self) -> None:
        self._birthdays: list[BirthdayEntry] = []

    @property
    def birthdays(self) -> list[BirthdayEntry]:
        return self._birthdays

    def add_birthday(self, person_name: str, birthday: str) -> None:
        if self.find_birthday(person_name) is not None:
            raise ValueError("Birthday for this person already exists.")
        entry = BirthdayEntry(person_name, birthday)
        self._birthdays.append(entry)

    def remove_birthday(self, person_name: str) -> bool:
        entry = self.find_birthday(person_name)
        if entry is None:
            return False
        self._birthdays.remove(entry)
        return True

    def find_birthday(self, person_name: str) -> BirthdayEntry | None:
        for entry in self._birthdays:
            if entry.person_name.lower() == person_name.lower():
                return entry
        return None

    def get_upcoming_birthdays(
        self,
        current_date: date,
        days_ahead: int = 7,
    ) -> list[BirthdayEntry]:
        upcoming = []
        for entry in self._birthdays:
            if entry.is_upcoming(current_date, days_ahead):
                upcoming.append(entry)
        return sorted(
            upcoming,
            key=lambda entry: entry.days_until_birthday(current_date),
        )

    def get_today_birthdays(self, current_date: date) -> list[BirthdayEntry]:
        return [entry for entry in self._birthdays if entry.is_today(current_date)]

    def to_dict(self) -> list[dict[str, Any]]:
        return [entry.to_dict() for entry in self._birthdays]

    def load_from_dict(self, data: list[dict[str, Any]]) -> None:
        self._birthdays = [BirthdayEntry.from_dict(item) for item in data]


class User:
    def __init__(self, username: str, email: str) -> None:
        self.username = username
        self.email = email
        self._reminder_book = ReminderBook()

    @property
    def username(self) -> str:
        return self._username

    @username.setter
    def username(self, value: str) -> None:
        if not value or not value.strip():
            raise ValueError("Username cannot be empty.")
        self._username = value.strip()

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        if "@" not in value or "." not in value:
            raise ValueError("Email is not valid.")
        self._email = value.strip()

    @property
    def reminder_book(self) -> ReminderBook:
        return self._reminder_book

    def add_birthday(self, person_name: str, birthday: str) -> None:
        self._reminder_book.add_birthday(person_name, birthday)

    def remove_birthday(self, person_name: str) -> bool:
        return self._reminder_book.remove_birthday(person_name)

    def get_upcoming_birthdays(
        self,
        current_date: date,
        days_ahead: int = 7,
    ) -> list[BirthdayEntry]:
        return self._reminder_book.get_upcoming_birthdays(current_date, days_ahead)

    def to_dict(self) -> dict[str, Any]:
        return {
            "username": self._username,
            "email": self._email,
            "birthdays": self._reminder_book.to_dict(),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "User":
        user = cls(data["username"], data["email"])
        user.reminder_book.load_from_dict(data.get("birthdays", []))
        return user


class NotificationSender(ABC):
    @abstractmethod
    def send(self, user: User, birthday_entry: BirthdayEntry) -> None:
        pass


class ConsoleNotificationSender(NotificationSender):
    def send(self, user: User, birthday_entry: BirthdayEntry) -> None:
        print(
            f"Reminder for {user.username}: today is {birthday_entry.person_name}'s birthday!"
        )


class ListNotificationSender(NotificationSender):
    def __init__(self) -> None:
        self.messages: list[str] = []

    def send(self, user: User, birthday_entry: BirthdayEntry) -> None:
        message = (
            f"Reminder for {user.username}: today is {birthday_entry.person_name}'s birthday!"
        )
        self.messages.append(message)


class ReminderManager:
    _instance: "ReminderManager | None" = None

    def __new__(cls) -> "ReminderManager":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._users = {}
        return cls._instance

    def add_user(self, user: User) -> None:
        if user.username in self._users:
            raise ValueError("User already exists.")
        self._users[user.username] = user

    def remove_user(self, username: str) -> bool:
        if username not in self._users:
            return False
        del self._users[username]
        return True

    def get_user(self, username: str) -> User | None:
        return self._users.get(username)

    def get_all_users(self) -> list[User]:
        return list(self._users.values())

    def save_to_file(self, filename: str) -> None:
        data = {username: user.to_dict() for username, user in self._users.items()}
        path = Path(filename)
        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    def load_from_file(self, filename: str) -> None:
        path = Path(filename)
        if not path.exists():
            self._users = {}
            return

        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        self._users = {
            username: User.from_dict(user_data)
            for username, user_data in data.items()
        }

    def send_today_notifications(
        self,
        sender: NotificationSender,
        current_date: date | None = None,
    ) -> None:
        if current_date is None:
            current_date = date.today()

        for user in self._users.values():
            today_birthdays = user.reminder_book.get_today_birthdays(current_date)
            for entry in today_birthdays:
                sender.send(user, entry)

    def clear_all(self) -> None:
        self._users = {}


def print_user_birthdays(user: User, current_date: date | None = None) -> None:
    if current_date is None:
        current_date = date.today()

    upcoming = user.get_upcoming_birthdays(current_date)

    print(f"\nUpcoming birthdays for {user.username}:")
    if not upcoming:
        print("No upcoming birthdays.")
        return

    for entry in upcoming:
        days_left = entry.days_until_birthday(current_date)
        print(
            f"- {entry.person_name}: {entry.birthday} (in {days_left} day(s))"
        )


def demo() -> None:
    manager = ReminderManager()
    manager.clear_all()

    user1 = User("naglis", "naglis@email.com")
    user2 = User("anna", "anna@email.com")

    user1.add_birthday("Jonas", "2000-04-10")
    user1.add_birthday("Mantas", "1999-04-15")
    user2.add_birthday("Ema", "2001-04-10")

    manager.add_user(user1)
    manager.add_user(user2)

    demo_date = date(2026, 4, 10)

    print("=== USERS AND UPCOMING BIRTHDAYS ===")
    print_user_birthdays(user1, demo_date)
    print_user_birthdays(user2, demo_date)

    print("\n=== TODAY NOTIFICATIONS ===")
    sender = ConsoleNotificationSender()
    manager.send_today_notifications(sender, demo_date)

    print("\n=== SAVE TO FILE ===")
    manager.save_to_file("birthdays.json")
    print("Data saved to birthdays.json")

    print("\n=== LOAD FROM FILE ===")
    manager.clear_all()
    manager.load_from_file("birthdays.json")
    print("Users loaded:", [user.username for user in manager.get_all_users()])

    print("\n=== SINGLETON CHECK ===")
    manager2 = ReminderManager()
    print("manager is manager2:", manager is manager2)


if __name__ == "__main__":
    demo()
