from collections import UserDict
from datetime import datetime, timedelta
import re

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\+?\d{10,15}", value):
            raise ValueError("Invalid phone number format. Use +XXXXXXXXXXX")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            date_value = datetime.strptime(value, "%d.%m.%Y").date()
            super().__init__(date_value)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Old phone not found")

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already exists for this contact.")
        self.birthday = Birthday(birthday)

    def days_to_birthday(self):
        if not self.birthday:
            return None
        today = datetime.now().date()
        next_birthday = self.birthday.value.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        bday = (
            self.birthday.value.strftime("%d.%m.%Y")
            if self.birthday
            else "—"
        )
        return f"{self.name.value}: {phones}; Birthday: {bday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.now().date()
        upcoming = []
        for record in self.data.values():
            if not record.birthday:
                continue

            next_birthday = record.birthday.value.replace(year=today.year)
            if next_birthday < today:
                next_birthday = next_birthday.replace(year=today.year + 1)

            if next_birthday.weekday() >= 5:
                next_birthday += timedelta(days=7 - next_birthday.weekday())

            days_left = (next_birthday - today).days
            if 0 <= days_left <= 7:
                upcoming.append({
                    "name": record.name.value,
                    "birthday": next_birthday.strftime("%d.%m.%Y"),
                    "days_left": days_left,
                })
        return upcoming