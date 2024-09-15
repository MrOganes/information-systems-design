import re
from datetime import datetime


class CustomerShortInfo:
    def __init__(self, customer_id, first_name, last_name, email):
        self.__customer_id = self.__validate_id(customer_id)
        self.__first_name = self.__validate_name(first_name)
        self.__last_name = self.__validate_name(last_name)
        self.__email = self.__validate_email(email)

    @staticmethod
    def from_string(data_str):
        try:
            # Предполагаем, что строка имеет формат: "id,first_name,last_name,email"
            data = data_str.split(',')
            if len(data) != 4:
                raise ValueError("Incorrect number of fields in the string.")

            customer_id = int(data[0].strip())
            first_name = data[1].strip()
            last_name = data[2].strip()
            email = data[3].strip()

            return CustomerShortInfo(customer_id, first_name, last_name, email)
        except Exception as e:
            raise ValueError(f"Error parsing CustomerShortInfo data: {e}")

    @staticmethod
    def __validate_id(customer_id):
        if isinstance(customer_id, int) and customer_id > 0:
            return customer_id
        raise ValueError("CustomerShortInfo ID must be a positive integer.")

    @staticmethod
    def __validate_name(name):
        if isinstance(name, str) and name:
            return name
        raise ValueError("Name must be a non-empty string up to 255 characters.")

    @staticmethod
    def __validate_email(email):
        email_regex = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+"
        if isinstance(email, str) and re.match(email_regex, email):
            return email
        raise ValueError("Invalid email format.")

    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def set_first_name(self, first_name):
        self.__first_name = self.__validate_name(first_name)

    def set_last_name(self, last_name):
        self.__last_name = self.__validate_name(last_name)

    def set_email(self, email):
        self.__email = self.__validate_email(email)

    def __eq__(self, other):
        if isinstance(other, CustomerShortInfo):
            return (self.__customer_id == other.__customer_id and
                    self.__first_name == other.__first_name and
                    self.__last_name == other.__last_name and
                    self.__email == other.__email)
        return False

    def __str__(self):
        return f"Customer short info [ID: {self.__customer_id}, Name: {self.__first_name} {self.__last_name}, Email: {self.__email}]"


class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone_number,
                 address, city, postal_code, country, date_joined):
        self.__customer_id = self.__validate_id(customer_id)
        self.__first_name = self.__validate_name(first_name)
        self.__last_name = self.__validate_name(last_name)
        self.__email = self.__validate_email(email)
        self.__phone_number = self.__validate_phone_number(phone_number)
        self.__address = self.__validate_non_empty_string(address, "Address")
        self.__city = self.__validate_non_empty_string(city, "City")
        self.__postal_code = self.__validate_postal_code(postal_code)
        self.__country = self.__validate_non_empty_string(country, "Country")
        self.__date_joined = self.__validate_date_joined(date_joined)

    # Статический метод для создания объекта из строки
    @staticmethod
    def from_string(data_str):
        try:
            # Предполагаем, что строка имеет формат: "id,first_name,last_name,email,phone_number,address,city,postal_code,country,date_joined"
            data = data_str.split(',')
            if len(data) != 10:
                raise ValueError("Incorrect number of fields in the string.")

            customer_id = int(data[0].strip())
            first_name = data[1].strip()
            last_name = data[2].strip()
            email = data[3].strip()
            phone_number = data[4].strip()
            address = data[5].strip()
            city = data[6].strip()
            postal_code = int(data[7].strip())
            country = data[8].strip()
            date_joined = data[9].strip()

            # Создание и возврат объекта Customer
            return Customer(customer_id, first_name, last_name, email, phone_number, address, city, postal_code,
                            country, date_joined)
        except Exception as e:
            raise ValueError(f"Error parsing customer data: {e}")

    # Getters
    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_city(self):
        return self.__city

    def get_postal_code(self):
        return self.__postal_code

    def get_country(self):
        return self.__country

    def get_date_joined(self):
        return self.__date_joined

    # Setters с валидацией
    def set_first_name(self, first_name):
        self.__first_name = self.__validate_name(first_name)

    def set_last_name(self, last_name):
        self.__last_name = self.__validate_name(last_name)

    def set_email(self, email):
        self.__email = self.__validate_email(email)

    def set_phone_number(self, phone_number):
        self.__phone_number = self.__validate_phone_number(phone_number)

    def set_address(self, address):
        self.__address = self.__validate_non_empty_string(address, "Address")

    def set_city(self, city):
        self.__city = self.__validate_non_empty_string(city, "City")

    def set_postal_code(self, postal_code):
        self.__postal_code = self.__validate_postal_code(postal_code)

    def set_country(self, country):
        self.__country = self.__validate_non_empty_string(country, "Country")

    def set_date_joined(self, date_joined):
        self.__date_joined = self.__validate_date_joined(date_joined)

    # Статические методы валидации
    @staticmethod
    def __validate_id(customer_id):
        if isinstance(customer_id, int) and customer_id > 0:
            return customer_id
        raise ValueError("Customer ID must be a positive integer.")

    @staticmethod
    def __validate_name(name):
        if isinstance(name, str) and name:
            return name
        raise ValueError("Name must be a non-empty string up to 255 characters.")

    @staticmethod
    def __validate_email(email):
        email_regex = r"[a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+"
        if isinstance(email, str) and re.match(email_regex, email):
            return email
        raise ValueError("Invalid email format.")

    @staticmethod
    def __validate_phone_number(phone_number):
        phone_regex = r"^\+?[0-9]{10,15}$"
        if isinstance(phone_number, str) and re.match(phone_regex, phone_number):
            return phone_number
        raise ValueError("Phone number must be a valid string with 10 to 15 digits, optionally starting with +.")

    @staticmethod
    def __validate_non_empty_string(value, field_name):
        if isinstance(value, str) and value.strip():
            return value
        raise ValueError(f"{field_name} must be a non-empty string.")

    @staticmethod
    def __validate_postal_code(postal_code):
        if isinstance(postal_code, int) and len(str(postal_code)) <= 10:
            return postal_code
        raise ValueError("Postal Code must be an integer with up to 10 digits.")

    @staticmethod
    def __validate_date_joined(date_joined):
        try:
            if isinstance(date_joined, str):
                return datetime.strptime(date_joined, '%Y-%m-%d %H:%M:%S')
            elif isinstance(date_joined, datetime):
                return date_joined
        except ValueError:
            raise ValueError("Date Joined must be a valid datetime in the format YYYY-MM-DD HH:MM:SS.")

    # Полная версия объекта
    def __str__(self):
        return (f"Customer [ID: {self.__customer_id}, Name: {self.__first_name} {self.__last_name}, "
                f"Email: {self.__email}, Phone: {self.__phone_number}, Address: {self.__address}, "
                f"City: {self.__city}, Postal Code: {self.__postal_code}, Country: {self.__country}, "
                f"Date Joined: {self.__date_joined.strftime('%Y-%m-%d %H:%M:%S')}]")

    # Краткая версия объекта (ключевая информация)
    def short_info(self):
        return f"Customer [ID: {self.__customer_id}, Name: {self.__first_name} {self.__last_name}, Email: {self.__email}]"

    # Метод для сравнения объектов
    def __eq__(self, other):
        if isinstance(other, Customer):
            return (self.__customer_id == other.__customer_id and
                    self.__first_name == other.__first_name and
                    self.__last_name == other.__last_name and
                    self.__email == other.__email and
                    self.__phone_number == other.__phone_number and
                    self.__address == other.__address and
                    self.__city == other.__city and
                    self.__postal_code == other.__postal_code and
                    self.__country == other.__country and
                    self.__date_joined == other.__date_joined)
        return False
