from collections import UserDict
from datetime import datetime
import pickle
import re


# Об'єкти класу "адресна книга"
class AddressBook(UserDict):
    # Функція, що записує контакт до адресної книги
    def add_record(self, Record):
        self.update({Record.Name.name: Record})
        return "Done!"

    # Функція, що виводить Номери телефону певного контакту
    def show_number(self, Name):
        return self.data[Name.name].Phones.phone

#    # Функція, що вовидить за раз N-ну кількість контактів із адресної книги (за замовчуванням виведе всі)
#    def iterator(self, N=None):
#        index = 0
#        N = len(self.data) if not N else N
#        while index < len(self.data):
#            yield list(self.data)[index: index + N]
#            index += N

    # Функція, що виводить спbсок всіх контактів, що містяться у адресній книзі
    def show_all(self):
        for name, info in self.data.items():
            yield f'{name} {info.Phones.phone} {info.Emails.email} {info.Birthday.birthday} {info.Address.address}'

#    # Функція, що шукає контакти, які містять певну послідовність літер в умені контакту, або чисел у його телефонних номерах
#    def find(self, piece_of_info):
#        res = []
#        for name, numbers in self.data.items():
#            if piece_of_info in name or piece_of_info in str(numbers.Phones.phone):
#                res.append(name)
#        if res:
#            for name in res:
#                print(f'{name}: {self.data[name].Phones.phone}')
#        else:
#            print('No matches')

    # Функція, що дозволяє зберігти наявну адресну книгу у файл на ПК
    def save_to_file(self, filename):
        with open(filename, "w+") as file:
            file.write('{:^20}|{:^40}|{:^70}|{:^10}|{:^50}\n'.format("Name", "Phones", "Emails", "Birthday", "Address"))
            for name, info in self.data.items():
                phones = ', '.join(info.Phones.phone)
                emails = ', '.join(info.Emails.email)
                file.write('{:^20}|{:^40}|{:^70}|{:^10}|{:^50}\n'.format(
                    name, phones, emails, info.Birthday.birthday, info.Address.address))


#    # Функція, що дозволяє завантажити адресну книгу з файлу на ПК
#    def read_from_file(self, filename):
#        with open(filename, "rb") as file:
#            content = pickle.load(file)
#        return content


# Об'єкти класу "контакт", що міститеме всю інформацію про нього
class Record:
    def __init__(self, Name, Phones=None, Birthday=None, Emails=None, Address=None):
        self.Name = Name
        self.Phones = Phones
        self.Birthday = Birthday
        self.Emails = Emails
        self.Address = Address

    # функція, що додає номер телефону до контакту
    def add_phone(self, Phone):
        self.Phones.phone = list(set(self.Phones.phone) | set(Phone.phone))
        return "Done!"

#    # Функція, що змінює наявні номери телефону на нові
#    def change_phone(self, Phone):
#        self.Phones = Phone
#       return "Done!"

#    # Функція, що видаляє наявний номер телефону
#    def delite_phone(self, Phone):
#        self.Phones.phone = list(set(self.Phones.phone) - set(Phone.phone))
#        return "Done!"

#    # Функція, що розраховує кількість днів до наступного дня нородження контакта
#    def days_to_birthday(self):
#        if self.Birthday.birthday:
#            current_datetime = datetime.now()
#            birthday = datetime.strptime(self.Birthday.birthday, '%d/%m/%Y')
#            if int(current_datetime.month) > int(birthday.month) or (int(current_datetime.month) == int(birthday.month) and int(current_datetime.day) >= int(birthday.day)):
#                next_birthday = datetime(
#                    year=current_datetime.year+1, month=birthday.month, day=birthday.day)
#                return f"In {(next_birthday - current_datetime).days} days"
#            else:
#                next_birthday = datetime(
#                    year=current_datetime.year, month=birthday.month, day=birthday.day)
#                return f"In {(next_birthday - current_datetime).days} days"
#        else:
#            return "The birthsay date is unknown."


# Після отримання введеної користувачем команди та відокремлення від неї слова-ключа, отримана інформація сортується за критеріями
class Field:
    def __init__(self, data):
        # Відокремлюються всі слова та обєднує їх у "ім'я" контакту
        self.name = re.findall('[a-z]+\s?[a-z]+\s?[a-z]+', data)[0]
        # Відокремлюються всі номери
        self.phone = re.findall('\d+', data)
        # Відокремлення дату, що має формат дд/мм/рррр (мається на увазі, що вона має бути введена тільки одна)
        self.birthday = ''.join(re.findall('\d{2}\/\d{2}\/\d{4}', data))
        # Відокремлює всі адреси електронної пошти
        self.email = re.findall('[A-Za-z][A-Za-z0-9_.]+@[A-Za-z]+\.[A-Za-z]{2,}', data)
        # Відокремлює адресу контакту
        self.address = ''.join(re.findall('\/[a-zA-Z-.\s]+\/[a-zA-Z0-9-.\s]+\/?[a-zA-Z0-9-.\s]*\/?[a-zA-Z0-9-.\s]*\/?[a-zA-Z0-9-.\s]*', data))


# Об'єкти класу "ім'я контакту"
class Name(Field):
    def __init__(self, name):
        super().__init__(name)


# Об'єкти класу "номер телефону"
class Phone(Field):
    def __init__(self, phone):
        self.__phone = None
        super().__init__(phone)

    @property
    def phone(self):
        return self.__phone

    # Перевірка на коректність вводу номерів телефону (мають містити від 10 до 12 чисел)
    @phone.setter
    def phone(self, phone):
        correct_numbers = []
        for number in phone:
            if 10 <= len(number) <= 12:
                correct_numbers.append(number)
        self.__phone = correct_numbers


# Обєкти класу "день народження"
class Birthday(Field):
    def __init__(self, birthday):
        self.__birthday = ''
        super().__init__(birthday)

    @property
    def birthday(self):
        return self.__birthday

    # Перевірка на коректність вводу (має бути формат дд/мм/рррр)
    @birthday.setter
    def birthday(self, birthday):
        try:
            birthday = birthday[:10]
            test = datetime.strptime(birthday, '%d/%m/%Y')
            current_datetime = datetime.now()
            if (current_datetime - test).days > 0:
                self.__birthday = birthday
        except:
            pass


# Обєкти класу "електронна пошта"
class Email(Field):
    def __init__(self, email):
        super().__init__(email)


# Обєкти класу "адреса"
class Address(Field):
    def __init__(self, address):
        super().__init__(address)

# Наша адресна книга
CONTACTS = AddressBook()


# Функція привітання
#def hello():
#    return 'How can I help you?'


# Фунція виходу
def close():
    CONTACTS.save_to_file('address_book.txt')
    return "The address book is saved to a file 'address_book.txt'. See You later!"


# Уникання будь-яких помилок під час роботи програми
def input_error(func):
    def inner():
        flag = True
        while flag:
            try:
                result = func()
                flag = False
            except IndexError:
                print('Enter the name and numbers separated by a space.')
            except ValueError:
                print('I have no idea how you did it, try again.')
            except KeyError:
                print("The contact is missing.")
        return result
    return inner


# Головна функція, куди додаємо весь функціонал
@ input_error
def main():
    bot_status = True
    # Умава, що забеспечує безкінечний цикл запиту, поки не буде виходу
    while bot_status:
        # Введення команди з консолі
        command = input('Enter the command: ').lower()
#        # Привітання з користувачем (сюди можна вставити правила вводу всіх можливих функцій)
#        if command == 'hello':
#            print(hello())
        # Додавання нового контакту
        if 'add' in command:
            command = command.removeprefix('add ')
            if Name(command).name in CONTACTS.data:
                print(CONTACTS.data[Name(command).name].add_phone(
                    Phone(command)))
            # Додавання нової інформації до вже існуючого контакту
            else:
                print(CONTACTS.add_record(
                    Record(Name(command), Phone(command), Birthday(command), Email(command), Address(command))))
#        # Зміна номеру телефону у вже існуючому контакті
#        elif "change" in command:
#            command = command.removeprefix('change ')
#            print(CONTACTS.data[Name(command).name].change_phone(Phone(command)))
#        # Видалення номеру телефону з вже існуючого контакту
#        elif "delite" in command:
#            command = command.removeprefix('delite ')
#            print(CONTACTS.data[Name(command).name].delite_phone(Phone(command)))
        # Вивід всіх існуючих номерів телефону певного контакту (вказувати ім'я після пробілу)
        elif "phone" in command:
            command = command.removeprefix("phone ")
            print(CONTACTS.show_number(Name(command)))
        # Вивід всіх існуючих контактів у адресній книзі
        elif command == "show all":
            if CONTACTS:
                for contact in CONTACTS.show_all():
                    print(contact)
            else:
                print('The contact list is empty.')
#        # Вивід кількості днів до наступного дня народження певного контакту із тих, що маються
#        elif "birthday" in command:
#            command = command.removeprefix("birthday ")
#            print(CONTACTS.data[Name(command).name].days_to_birthday())
#        # Пошук контакту за певною послідовністю літер або чисел
#        elif "find" in command:
#            command = command.removeprefix('find ')
#            CONTACTS.find(command)
        # Вихід із програми (сюди треба додати автоматичне збереження наявної адресної книги)
        elif command in ("good bye", "bye", "close", "exit", "end"):
            print(close())
            bot_status = False
        # Якщо користувач некоректно ввів команду (тут можна реалізувати додаткове завдання з підказкою можливих команд)
        else:
            print("Enter correct command, please.")

rules = '''
Hello! Welcome to Address Book.

Available commands:
"add [name]* [phones]** [emails]** [birthday]** [address]**" - adds a new contact to the address book
    name - no more than three words
    phones - can be several (each must contain 10 to 12 digits), enter with a space
    emails - can be several, enter with a space
    birthday - date in format dd/mm/yyyy (must be only one)
    address - must contain at least a street and a house number, all elements must be separated by a slash and start with a slash (example: /United States/New York/Atlantic st./3-B)
"phone [name]*" - shows phone numbers of a particular contact
"show all" - show you full list of contacts in the address book
"good bye", "bye", "close", "exit" or "end" - exit the address book and save it in file "address_book.txt"

* - mandatory field
** - optional field
'''

if __name__ == '__main__':
    print(rules)
    main()
