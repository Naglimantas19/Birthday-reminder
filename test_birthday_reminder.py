import os
import tempfile
import unittest
from datetime import date

from birthday_reminder import (
    BirthdayEntry,
    ListNotificationSender,
    ReminderManager,
    User,
)


class BirthdayReminderTests(unittest.TestCase):
    def setUp(self):
        self.manager = ReminderManager()
        self.manager.clear_all()

    def test_add_birthday(self):
        user = User("naglis", "naglis@email.com")
        user.add_birthday("Jonas", "2000-04-10")

        self.assertEqual(len(user.reminder_book.birthdays), 1)
        self.assertEqual(user.reminder_book.birthdays[0].person_name, "Jonas")

    def test_remove_birthday(self):
        user = User("naglis", "naglis@email.com")
        user.add_birthday("Jonas", "2000-04-10")
        removed = user.remove_birthday("Jonas")

        self.assertTrue(removed)
        self.assertEqual(len(user.reminder_book.birthdays), 0)

    def test_upcoming_birthdays(self):
        user = User("naglis", "naglis@email.com")
        user.add_birthday("Jonas", "2000-04-10")
        user.add_birthday("Mantas", "2000-04-20")

        upcoming = user.get_upcoming_birthdays(date(2026, 4, 8), 5)
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].person_name, "Jonas")

    def test_today_notification(self):
        user = User("naglis", "naglis@email.com")
        user.add_birthday("Jonas", "2000-04-10")
        self.manager.add_user(user)

        sender = ListNotificationSender()
        self.manager.send_today_notifications(sender, date(2026, 4, 10))

        self.assertEqual(len(sender.messages), 1)
        self.assertIn("Jonas", sender.messages[0])

    def test_singleton_manager(self):
        manager1 = ReminderManager()
        manager2 = ReminderManager()

        self.assertIs(manager1, manager2)

    def test_save_and_load_file(self):
        user = User("naglis", "naglis@email.com")
        user.add_birthday("Jonas", "2000-04-10")
        self.manager.add_user(user)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as tmp:
            filename = tmp.name

        try:
            self.manager.save_to_file(filename)
            self.manager.clear_all()
            self.manager.load_from_file(filename)

            loaded_user = self.manager.get_user("naglis")
            self.assertIsNotNone(loaded_user)
            self.assertEqual(len(loaded_user.reminder_book.birthdays), 1)
        finally:
            if os.path.exists(filename):
                os.remove(filename)

    def test_invalid_date_raises_error(self):
        with self.assertRaises(ValueError):
            BirthdayEntry("Jonas", "10-04-2000")


if __name__ == "__main__":
    unittest.main()
