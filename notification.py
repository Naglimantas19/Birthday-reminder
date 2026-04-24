from abc import ABC, abstractmethod


class NotificationSender(ABC):
    @abstractmethod
    def send(self, user, birthday_entry):
        pass


class ConsoleNotificationSender(NotificationSender):
    def send(self, user, birthday_entry):
        print(
            f"Reminder for {user.username}: today is {birthday_entry.person_name}'s birthday!"
        )


class ListNotificationSender(NotificationSender):
    def __init__(self):
        self.messages = []

    def send(self, user, birthday_entry):
        message = (
            f"Reminder for {user.username}: today is {birthday_entry.person_name}'s birthday!"
        )
        self.messages.append(message)