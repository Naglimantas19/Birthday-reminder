from datetime import date

from manager import ReminderManager
from notification import ConsoleNotificationSender
from user import User


def print_user_birthdays(user, current_date=None):
    if current_date is None:
        current_date = date.today()

    upcoming = user.get_upcoming_birthdays(current_date)

    print(f"\nUpcoming birthdays for {user.username}:")

    if not upcoming:
        print("No upcoming birthdays.")
        return

    for entry in upcoming:
        days_left = entry.days_until_birthday(current_date)
        print(f"- {entry.person_name}: {entry.birthday} (in {days_left} day(s))")


def demo():
    manager = ReminderManager()
    manager.clear_all()

    user1 = User("naglis", "naglis@email.com")
    user2 = User("anna", "anna@email.com")

    user1.add_birthday("Jonas", "2000-05-07")
    user1.add_birthday("Mantas", "1999-08-15")
    user2.add_birthday("Ema", "2001-04-10")

    manager.add_user(user1)
    manager.add_user(user2)

    demo_date = date.today()

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
