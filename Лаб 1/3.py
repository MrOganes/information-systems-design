class Customer:
    def __init__(self, customer_id, first_name, last_name, email, phone_number, address, city, postal_code, country, date_joined):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
        self.__address = address
        self.__city = city
        self.__postal_code = postal_code
        self.__country = country
        self.__date_joined = date_joined

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

    # Setters
    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_address(self, address):
        self.__address = address

    def set_city(self, city):
        self.__city = city

    def set_postal_code(self, postal_code):
        self.__postal_code = postal_code

    def set_country(self, country):
        self.__country = country

    def set_date_joined(self, date_joined):
        self.__date_joined = date_joined
