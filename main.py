from collections import UserDict
from typing import List
from datetime import datetime, timedelta
import re
import json


class Field:
    def __init__(self, value: str) -> None:
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    @Field.value.setter
    def value(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Name not a string")
        self._value = value


class Phone(Field):
    @Field.value.setter
    def value(self, value: str) -> None:
        if (len(value) == 13 or len(value) == 10 or len(value) == 12 or len(value) == 9) and (
                value.startswith("380")
                or value.startswith("+380") or value.startswith("0") or value.startswith("+0")):
            self._value = value
        else:
            raise ValueError


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str):
        try:
            self._value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            print("Input hb in format 2000-07-09")


class Record:
    def __init__(self, name: Name, birthday: Birthday = None, phons: List[Phone] = []) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = phons

    def change_phone(self, phone: Phone, new_phone: Phone):
        if self.remove_record(phone):
            self.phones.append(new_phone)
            return new_phone

    def remove_record(self, phone: Phone):
        for i, phone in enumerate(self.phones):
            if phone.value == phone.value:
                return self.phones.pop(i)

    def __repr__(self) -> str:
        if not self.phones and not self.birthday:
            return f"{self.name.value.title()} not number"
        if not self.phones:
            return f"{self.name.value.title()} not number, birthday: {self.birthday.value}"
        if self.birthday is None:
            return f"{self.name.value.title()}:{[p.value for p in self.phones]}"
        else:
            return f"{self.name.value.title()}:{[p.value for p in self.phones]}, birtdate: {self.birthday.value}"

    def days_to_birthday(self, birthday: Birthday):
        time_now = datetime.now()
        pattern = self.birthday.value.replace(year=time_now.year)
        diff = pattern - time_now.date()
        if -365 <= diff.days <= -1:
            diff1 = 365 + diff.days
            return f"{diff1} days to birthday"
        else:
            return f"{diff.days} days to birthday"


class AddressBook(UserDict):

    def add_record(self, rec: Record):
        self.data[rec.name.value] = rec

    def iterator(self, max_count):
        count = 0
        for k in self.data:
            if count < max_count:
                count += 1
                yield self.data[k]
        else:
            raise StopIteration

    def show_c_w(self, value):
        ls = []
        if len(value[0]) >= 3:
            for k, v in ab.items():
                v = repr(v)
                [ls.append(v) for i in value if i.title() in v]
            return ls
        else:
            return "You must write 3+ words that find contact or contacts"

    def dump(self):
        with open("adressbook.json", "w", encoding="utf-8") as f:
            json.dump([f"{v}" for v in ab.values()], f, indent=2)

    def load(self):
        with open("adressbook.json", "r", encoding="utf-8") as f:
            return json.load(f)


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return """If you write command 'add' please write 'add' 'name' 'number'
If you write command 'change' please write 'change' 'name' 'number'
If you write command 'phone' please write 'phone' 'name'
If you write command 'remove' please write 'remove' 'name' 'number'"""
        except KeyError:
            return "This key not found try again"
        except TypeError:
            return "Type not supported try again"
        except ValueError:
            return "Incorrect value try again"
        except AttributeError:
            return "Incorrect attribute try again"
        except StopIteration:
            return "That's all"
        except RuntimeError:
            return "That's all"

    return wrapper


def input_help():
    return """help - output command, that help find command
hello - output command 'How can I help you?' 
add - add contact, use 'add' 'name' 'number'
change - change your contact, use 'change' 'name' 'number'
phone - use 'phone' 'name' that see number this contact
show all - show all your contacts
display - show N contacts, use "display", "N"
remove - remove contact, use "remove", "name", "number"
find - find the contact by letters > 3, use "find", "count"
"""


@input_error
def input_bye(*args):
    return "Good bye"


@input_error
def input_hello(*args):
    return "How can I help you?"


ab = AddressBook()


@input_error
def input_add(*args):
    name = Name(args[0])
    phone = Phone(args[1])
    try:
        birthday = Birthday(args[2])
    except IndexError:
        birthday = None
    rec = Record(name=name, phons=[phone], birthday=birthday)
    ab.add_record(rec)
    return f"Contact {rec.name.value.title()} add successful"


@input_error
def input_change(*args):
    phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec = ab.data[args[0]]
    result = rec.change_phone(phone, new_phone)
    if result:
        return f"Contact {rec.name.value.title()} change successful"


@input_error
def input_phone(*args):
    get_contact = repr(ab.get(args[0]))
    pattern = re.findall(r"\+?\d+", get_contact)
    return pattern[0]


@input_error
def input_show(*args):
    return "\n".join([f"{v} " for v in ab.values()])


@input_error
def input_remove(*args):
    phone = Phone(args[1])
    rec = ab.data[args[0]]
    result = rec.remove_record(phone)
    if result:
        return f"phone {phone.value} remove successful"


@input_error
def input_day_to_hb(*args):
    rec = ab[args[0]]
    result = (repr(rec))
    result1 = re.search(r"\d{4}-\d{2}-\d{2}", result)
    birt = Birthday(result1.group())
    rec_func = rec.days_to_birthday(birt)
    return rec_func


@input_error
def input_show_n(*args):
    for i in ab.iterator(int(args[0])):
        print(i)


@input_error
def input_show_txt(*args):
    str_contacts = ''
    if type(ab.show_c_w(args)) is str:
        return "You must write 3+ words that find contact or contacts"
    else:
        for i in ab.show_c_w(args):
            str_contacts += i + '\n'
        return str_contacts[:-1]


commands = {
    input_hello: "hello",
    input_add: "add",
    input_phone: "phone",
    input_show: "show all",
    input_change: "change",
    input_bye: "exit",
    input_help: "help",
    input_remove: "remove",
    input_day_to_hb: "birthday",
    input_show_n: "display",
    input_show_txt: "find"
}


def command_parser(user_input1):
    data = []
    command = ""
    for k, v in commands.items():
        if user_input1.startswith(v):
            command = k
            data = user_input1.replace(v, "").split()
        if user_input1 == "":
            main()
    return command, data


@input_error
def main():
    result = ab.load()
    for i in result:
        print(i)
    while True:
        user_input = input(">>>")
        user_input1 = user_input.lower()
        command, data = command_parser(user_input1)
        if command == "display":
            command(*data)
        else:
            print(command(*data))
        if command == input_bye:
            ab.dump()
            break


if __name__ == "__main__":
    main()
