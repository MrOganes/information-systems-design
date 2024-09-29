import json
import re
from datetime import datetime

import psycopg2 as psycopg2
import yaml
from psycopg2.extras import DictCursor


class CustomerShortInfo:
    def __init__(self, customer_id, first_name, last_name, email):
        self.set_id(customer_id)
        self.set_first_name(first_name)
        self.set_last_name(last_name)
        self.set_email(email)

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

    def set_id(self, customer_id):
        self.__customer_id = self.__validate_id(customer_id)

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

    def __hash__(self):
        return hash(self.get_first_name()) + hash(self.get_last_name()) + hash(self.get_customer_id()) + hash(
            self.get_email())


class Customer(CustomerShortInfo):
    def __init__(self, customer_id, first_name, last_name, email, phone_number=None,
                 address=None, city=None, postal_code=None, country=None, date_joined=None):
        super().__init__(customer_id, first_name, last_name, email)
        if phone_number:
            self.set_phone_number(phone_number)
        if address:
            self.set_address(address)
        if city:
            self.set_city(city)
        if postal_code:
            self.set_postal_code(postal_code)
        if country:
            self.set_country(country)
        if date_joined:
            self.set_date_joined(date_joined)

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

            return Customer(customer_id, first_name, last_name, email, phone_number, address, city, postal_code,
                            country, date_joined)
        except Exception as e:
            raise ValueError(f"Error parsing customer data: {e}")

    @staticmethod
    def from_dict(data: dict):
        date_time = datetime.strptime(data['date_joined'], '%Y-%m-%d %H:%M:%S') if data.get('date_joined') else None
        return Customer(
            data['customer_id'],
            data['first_name'],
            data['last_name'],
            data['email'],
            data.get('phone_number'),
            data.get('address'),
            data.get('city'),
            data.get('postal_code'),
            data.get('country'),
            date_time
        )

    def to_dict(self):
        return {
            'customer_id': self.get_customer_id(),
            'first_name': self.get_first_name(),
            'last_name': self.get_last_name(),
            'email': self.get_email(),
            'phone_number': self.get_phone_number() if hasattr(self, 'phone_number') else None,
            'address': self.get_address() if hasattr(self, 'address') else None,
            'city': self.get_city() if hasattr(self, 'city') else None,
            'postal_code': self.get_postal_code() if hasattr(self, 'postal_code') else None,
            'country': self.get_country() if hasattr(self, 'country') else None,
            'date_joined': self.get_date_joined().strftime('%Y-%m-%d %H:%M:%S') if hasattr(self, 'date_joined') else None
        }

    def get_phone_number(self):
        if hasattr(self, '_Customer__phone_number'):
            return self.__phone_number
        return None

    def get_address(self):
        if hasattr(self, '_Customer__address'):
            return self.__address
        return None

    def get_city(self):
        if hasattr(self, '_Customer__city'):
            return self.__city
        return None

    def get_postal_code(self):
        if hasattr(self, '_Customer__postal_code'):
            return self.__postal_code
        return None

    def get_country(self):
        if hasattr(self, '_Customer__country'):
            return self.__country
        return None

    def get_date_joined(self):
        if hasattr(self, '_Customer__date_joined'):
            return self.__date_joined
        return None

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

    def __str__(self):
        return (f"Customer [ID: {self.get_customer_id()}, "
                f"Name: {self.get_first_name()} {self.get_last_name()}, "
                f"Email: {self.get_email()}, "
                f"Phone: {self.get_phone_number()}, "
                f"Address: {self.get_address()}, "
                f"City: {self.get_city()}, "
                f"Postal Code: {self.get_postal_code()}, "
                f"Country: {self.get_country()}, "
                f"Date Joined: {self.get_date_joined()}]")

    def short_info(self):
        return super().__str__()

    def __eq__(self, other):
        if isinstance(other, Customer):
            return super().__eq__(other)
        return False


class CustomerRepBase:
    def __init__(self, filename):
        self.filename = filename
        self.customers = self.read_all()

    # Чтение всех значений (должен быть реализован в дочерних классах)
    def read_all(self):
        raise NotImplementedError("Метод должен быть реализован в дочернем классе")

    # Запись всех значений (должен быть реализован в дочерних классах)
    def save_all(self):
        raise NotImplementedError("Метод должен быть реализован в дочернем классе")

    # Получить объект по ID
    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.get_customer_id() == customer_id:
                return customer
        raise ValueError(f"Customer with ID {customer_id} not found.")

    # Получить список k по счету объектов
    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return self.customers[start:end]

    # Сортировка элементов по выбранному полю
    def sort_by_field(self):
        self.customers.sort(key=lambda customer: customer.get_date_joined())

    # Проверка на уникальность ID и Email
    def __is_unique(self, email, unverifiable_customer_id=None):
        if unverifiable_customer_id:
            for customer in self.customers:
                if customer.get_customer_id() != unverifiable_customer_id and customer.get_email() == email:
                    return False
        else:
            for customer in self.customers:
                if customer.get_email() == email:
                    return False
        return True

    # Добавление объекта (формируется новый ID)
    def add_customer(self, customer):
        new_id = max([customer.get_customer_id() for customer in self.customers], default=0) + 1
        customer.set_id(new_id)

        if not self.__is_unique(customer.get_email()):
            raise ValueError(f"Customer with this email already exists.")

        self.customers.append(customer)
        self.save_all()

    # Замена элемента по ID
    def replace_by_id(self, customer_id, new_customer):
        if not self.__is_unique(new_customer.get_email(), customer_id):
            raise ValueError(f"Customer with this email already exists.")

        for i, customer in enumerate(self.customers):
            if customer.get_customer_id() == customer_id:
                self.customers[i] = new_customer
                self.save_all()
                return True
        return False

    # Удаление элемента по ID
    def delete_by_id(self, customer_id):
        self.customers = [customer for customer in self.customers if customer.get_customer_id() != customer_id]
        self.save_all()

    # Получить количество элементов
    def get_count(self):
        return len(self.customers)


class CustomerRepJson(CustomerRepBase):
    # Чтение всех значений из JSON-файла
    def read_all(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Customer.from_dict(customer) for customer in data]
        except FileNotFoundError:
            return []

    # Запись всех значений в JSON-файл
    def save_all(self):
        with open(self.filename, 'w') as file:
            json.dump([customer.to_dict() for customer in self.customers], file, indent=4)


class CustomerRepYaml(CustomerRepBase):
    # Чтение всех значений из YAML-файла
    def read_all(self):
        try:
            with open(self.filename, 'r') as file:
                data = yaml.safe_load(file) or []
                return [Customer.from_dict(customer) for customer in data]
        except FileNotFoundError:
            return []

    # Запись всех значений в YAML-файл
    def save_all(self):
        with open(self.filename, 'w') as file:
            yaml.safe_dump([customer.to_dict() for customer in self.customers], file, default_flow_style=False)


class DatabaseConnection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        if not hasattr(self, 'connection'):
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


class CustomerRepPostgres:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.db = DatabaseConnection(db_name, user, password, host, port)

    def add_customer(self, customer):
        query = """
            INSERT INTO customers (first_name, last_name, email, phone_number, address, city, postal_code, country, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING customer_id
        """
        data = customer.to_dict()
        self.db.execute(query, (data['first_name'], data['last_name'], data['email'], data['phone_number'],
                                data['address'], data['city'], data['postal_code'], data['country'],
                                data['date_joined']))
        new_id = self.db.fetchone()[0]
        self.db.commit()
        return new_id

    # Получить объект по ID
    def get_by_id(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = %s"
        self.db.execute(query, (customer_id,))
        data = self.db.fetchone()
        if data:
            return Customer(data['customer_id'], data['first_name'], data['last_name'], data['email'],
                            data.get('phone_number'), data.get('address'), data.get('city'), data.get('postal_code'),
                            data.get('country'), data.get('date_joined'))
        return None

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        query = "SELECT * FROM customers ORDER BY customer_id LIMIT %s OFFSET %s"
        self.db.execute(query, (n, offset))
        return self.db.fetchall()

    def replace_by_id(self, customer_id, new_customer):
        query = """
            UPDATE customers 
            SET first_name = %s, last_name = %s, email = %s, phone_number = %s, address = %s, city = %s, postal_code = %s, country = %s, date_joined = %s
            WHERE customer_id = %s
        """
        data = new_customer.to_dict()
        self.db.execute(query, (data['first_name'], data['last_name'], data['email'], data['phone_number'],
                                data['address'], data['city'], data['postal_code'], data['country'],
                                data['date_joined'], customer_id))
        self.db.commit()

    def delete_by_id(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = %s"
        self.db.execute(query, (customer_id,))
        self.db.commit()

    def get_count(self):
        query = "SELECT COUNT(*) FROM customers"
        self.db.execute(query)
        return self.db.fetchone()[0]


class CustomerRepPostgresAdapter(CustomerRepBase):
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        # Мы передаем filename как None, так как это не нужно для Postgres.
        super().__init__(None)
        self.rep_postgres = CustomerRepPostgres(db_name, user, password, host, port)

    # Реализуем методы для работы с Postgres
    def read_all(self):
        # Этот метод можно оставить пустым или возвращать данные из Postgres при необходимости.
        pass

    def save_all(self):
        # В случае с Postgres вызов этого метода может быть неактуальным, так как изменения сохраняются напрямую в БД.
        pass

    def add_customer(self, customer):
        return self.rep_postgres.add_customer(customer)

    def get_by_id(self, customer_id):
        return self.rep_postgres.get_by_id(customer_id)

    def get_k_n_short_list(self, k, n):
        return self.rep_postgres.get_k_n_short_list(k, n)

    def replace_by_id(self, customer_id, new_customer):
        return self.rep_postgres.replace_by_id(customer_id, new_customer)

    def delete_by_id(self, customer_id):
        return self.rep_postgres.delete_by_id(customer_id)

    def get_count(self):
        return self.rep_postgres.get_count()
