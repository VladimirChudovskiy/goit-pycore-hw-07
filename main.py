from task1 import AddressBook, Record

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (KeyError, ValueError, IndexError) as e:
            return f"Error: {str(e)}"
    return wrapper

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.edit_phone(old_phone, new_phone)
    return "Phone updated."


@input_error
def show_phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    return f"{name}: {'; '.join(p.value for p in record.phones)}"


@input_error
def show_all(args, book: AddressBook):
    if not book.data:
        return "Address book is empty."
    return "\n".join(str(r) for r in book.data.values())


@input_error
def add_birthday(args, book: AddressBook):
    name, date = args
    record = book.find(name)
    if not record:
        return "Contact not found."
    record.add_birthday(date)
    return f"Birthday added for {name}."


@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if not record:
        return "Contact not found."
    if record.birthday:
        return f"{name}'s birthday: {record.birthday.value.strftime('%d.%m.%Y')}"
    return f"{name} has no birthday set."


@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    if not upcoming:
        return "No birthdays this week."
    return "\n".join(f"{b['name']} — {b['birthday']} (через {b['days_left']} дн.)" for b in upcoming)

def parse_input(user_input):
    parts = user_input.strip().split()
    return parts[0].lower(), parts[1:]


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command == "add":
            print(add_contact(args, book))
        elif command == "change":
            print(change_contact(args, book))
        elif command == "phone":
            print(show_phone(args, book))
        elif command == "all":
            print(show_all(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        elif command == "birthdays":
            print(birthdays(args, book))
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()