from abc import ABC, abstractmethod


class ICustomerRepository(ABC):
    @abstractmethod
    def add_customer(self, customer):
        pass

    @abstractmethod
    def get_by_id(self, customer_id):
        pass

    @abstractmethod
    def get_k_n_short_list(self, k, n):
        pass

    @abstractmethod
    def replace_by_id(self, new_customer):
        pass

    @abstractmethod
    def delete_by_id(self, customer_id):
        pass

    @abstractmethod
    def get_count(self):
        pass