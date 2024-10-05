import json

from Customer import Customer
from FileStrategy import FileStrategy


class JsonFileStrategy(FileStrategy):
    def __init__(self, filename):
        self.filename = filename

    def read_all(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                return [Customer.from_dict(customer) for customer in data]
        except FileNotFoundError:
            return []

    def save_all(self, customers):
        with open(self.filename, 'w') as file:
            json.dump([customer.to_dict() for customer in customers], file, indent=4)