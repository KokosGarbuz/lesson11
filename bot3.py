import datetime

class Field:
    def __init__(self, value=None):
        self._value = value

    def __str__(self):
        return str(self._value)

    def get_value(self):
        return self._value

    def set_value(self, new_value):
        self.validate(new_value)
        self._value = new_value

    def validate(self, value):
        pass

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def validate(self, value):
        if value is not None and not isinstance(value, str):
            raise ValueError("Phone must be a string")
        if value is not None and not value.isdigit():
            raise ValueError("Phone must contain only digits")
        if value is not None and len(value) != 10:
            raise ValueError("Phone must be 10 digits long")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.set_value(new_value)

class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def validate(self, value):
        if value is not None:
            try:
                datetime.datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Use 'YYYY-MM-DD'")

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self.set_value(new_value)

class Record:
    def __init__(self, name, phone=None, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

        if phone:
            self.add_phone(phone)

    def add_phone(self, phone):
        phone_field = Phone(phone)
        self.phones.append(phone_field)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if str(phone) == old_phone:
                phone.set_value(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.date.today()
            next_birthday = datetime.date(today.year, self.birthday.value.month, self.birthday.value.day)
            if today > next_birthday:
                next_birthday = datetime.date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

    def __str__(self):
        phones_str = ', '.join(str(p) for p in self.phones)
        birthday_str = self.birthday.value if self.birthday.value else "N/A"
        return f"Name: {self.name}, Phones: {phones_str}, Birthday: {birthday_str}"

class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def remove_record(self, name):
        if name in self.data:
            del self.data[name]

    def find_records_by_name(self, name):
        return [record for record in self.data.values() if record.name.get_value() == name]

    def find_records_by_phone(self, phone):
        return [record for record in self.data.values() if any(str(p) == phone for p in record.phones)]

    def __iter__(self):
        self._iter_index = 0
        self._page_size = 5
        self._keys = list(self.data.keys())
        return self

    def __next__(self):
        if self._iter_index >= len(self._keys):
            raise StopIteration
        else:
            keys_slice = self._keys[self._iter_index:self._iter_index+self._page_size]
            records = [self.data[key] for key in keys_slice]
            self._iter_index += self._page_size
            return records

if __name__ == "__main__":
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").strip().lower()
        if command == "exit":
            break
        elif command == "add":
            name = input("Enter a name: ")
            birthday = input("Enter a birthday (optional, format YYYY-MM-DD): ")
            record = Record(name, birthday=birthday)
            while True:
                phone = input("Enter a phone (leave empty to finish): ").strip()
                if not phone:
                    break
                record.add_phone(phone)
            address_book.add_record(record)
        elif command == "remove":
            name = input("Enter a name to remove: ")
            address_book.remove_record(name)
        elif command == "find by name":
            name = input("Enter a name to find: ")
            found_records = address_book.find_records_by_name(name)
            for record in found_records:
                print(record)
        elif command == "find by phone":
            phone = input("Enter a phone to find: ")
            found_records = address_book.find_records_by_phone(phone)
            for record in found_records:
                print(record)
        elif command == "show all":
            for page, records in enumerate(address_book, start=1):
                print(f"Page {page}:")
                for record in records:
                    print(record)
                more_pages = (page * 5) < len(address_book.data)
                if more_pages:
                    print("More pages available. Type 'next' to see more.")
        elif command == "next":
            pass  
        else:
            print("Invalid command. Try again.")
