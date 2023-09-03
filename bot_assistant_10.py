import sys

from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, Record):
        self.data[Record.name.value] = Record

class Record:
    def __init__(self, Name):
        self.name = Name
        self.phones = []

    def add_phone(self, Phone):
        self.phones.append(Phone)

    def remove_phone(self, Rem_Phone):
        for Phone in self.phones:
            if Phone.value == Rem_Phone.value:
                self.phones.remove(Phone)

    def change_phone(self, Old_Phone, New_Phone):
        for Phone in self.phones:
            if Phone.value == Old_Phone.value:
                self.phones.remove(Phone)
                self.phones.append(New_Phone)

class Field:
    def __init__(self, value):
        self.value = value

class Name(Field):
    pass

class Phone(Field):
    pass

address_book = AddressBook()

def parse(user_input):
    """
    This function parse user input into command and arguments
    :param user_input: user input -> str
    :return: command -> str, args -> list
    """
    user_input_list = user_input.split(' ')
    command = user_input_list[0]
    args = user_input_list[1:]
    return (command, args)

def input_error(func):
    """
    This is a decorator function that catches errors that may occur when calling a function given as a parameter
    :param func -> function
    :return func if no error, str if there's an error
    """
    def inner(*args):
        try:
            return func(*args)
        except KeyError:
            return 'The name is not in contacts. Enter user name please'
        except ValueError:
            return 'ValueError: Give me name and phone please'
        except IndexError:
            return 'IndexError: Give me name and phone please'
        except TypeError:
            return 'You entered invalid numbers of arguments for this command'
    return inner

@input_error
def add_contact(name, phone=None):
    if name in address_book.data.keys():
        address_book.data[name].add_phone(Phone(phone))
        return f'Phone {phone} successfully added to contact {name}'
    else:
        record = Record(Name(name))
        record.add_phone(Phone(phone))
        address_book.add_record(record)
        return f'Contact {name} -> {phone} successfully added'

@input_error
def change_contact(name, old_phone, new_phone):
    """
    This function change the phone for contact with the name that are given as parameters in the address_book
    :param name -> str
           phone -> str
    :return str
    """
    address_book.data[name].change_phone(Phone(old_phone), Phone(new_phone))
    return f'Contact {name} -> {new_phone} successfully changed'

@input_error
def remove_phone(name, phone):
    """
    This function remove the phone for contact with the name that are given as parameters in the address_book
    :param name -> str
           phone -> str
    :return str
    """
    address_book.data[name].remove_phone(Phone(phone))
    return f'The phone {phone} for contact {name} successfully removed'

@input_error
def get_phone(name):
    """
    This function change the phone for contact with the name that are given as parameters in the address_book
    :param name -> str
    :return phone -> str
    """
    if not address_book.data[name].phones:
        return f'There is no phones for contact with name {name}'
    else:
        phones = 'phones:\n'
        for phone in address_book.data[name].phones:
            phones += f'{phone.value}\n'
        return f'{name} ->\n{phones}'

def show_all():
    """
    This function returns all contact from the address_book
    :param: None
    :return: phone_book -> str
    """
    phone_book = ''
    for name, info in address_book.data.items():
        phones = 'phones:\n'
        for phone in address_book.data[name].phones:
            phones += f'{phone.value}\n'
        phone_book += f'{name} ->\n{phones}\n'
    return phone_book

def greeting():
    return 'How can I help you?'

def end():
    return 'Good bye!'

def main():
    """
    This function implements all the logic of interaction with the user, all 'print' and 'input' takes place here
    :param: None
    :return: None
    """
    handler_commands = {'hello': greeting,
                        'hi': greeting,
                        'add': add_contact,
                        'change': change_contact,
                        'phone': get_phone,
                        'remove': remove_phone,
                        'show all': show_all,
                        '.': end,
                        'good bye': end,
                        'close': end,
                        'exit': end}

    while True:
        user_input = input('>>>:')
        if user_input.lower() in handler_commands.keys():
            output = handler_commands[user_input.lower()]()
            print(output)
            if output == 'Good bye!':
                sys.exit()
        else:
            command, args = parse(user_input.lower())
            if command in handler_commands.keys():
                print(handler_commands[command](*args))
            else:
                print(
                    "You entered an invalid command, please enter one of the next commands: "
                    "'hello', 'hi', 'show all', 'add', 'change', 'phone', 'delete', '.', 'good bye', 'close', 'exit'")


if __name__ == '__main__':
    main()