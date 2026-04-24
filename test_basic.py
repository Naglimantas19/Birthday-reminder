import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from user import User
from birthday_entry import BirthdayEntry
from manager import ReminderManager


class TestBirthdayApp(unittest.TestCase):

    def test_create_user(self):
        user = User("test", "test@email.com")
        self.assertEqual(user.username, "test")

    def test_add_birthday(self):
        user = User("test", "test@email.com")
        user.add_birthday("Jonas", "2000-01-01")
        self.assertEqual(len(user._birthdays), 1)

    def test_remove_birthday(self):
        user = User("test", "test@email.com")
        user.add_birthday("Jonas", "2000-01-01")
        user.remove_birthday("Jonas")
        self.assertEqual(len(user._birthdays), 0)

    def test_singleton_manager(self):
        m1 = ReminderManager()
        m2 = ReminderManager()
        self.assertTrue(m1 is m2)


if __name__ == "__main__":
    unittest.main()
