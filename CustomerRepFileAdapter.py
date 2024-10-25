from CustomerRepBase import CustomerRepBase
from ICustomerRepository import ICustomerRepository


class CustomerRepFileAdapter(ICustomerRepository):
    def __init__(self, strategy):
        self.rep_file = CustomerRepBase(strategy)

    def add_customer(self, customer):
        return self.rep_file.add_customer(customer)

    def get_by_id(self, customer_id):
        return self.rep_file.get_by_id(customer_id)

    def get_k_n_short_list(self, k, n):
        return self.rep_file.get_k_n_short_list(k, n)

    def replace_by_id(self, new_customer):
        return self.rep_file.replace_by_id(new_customer)

    def delete_by_id(self, customer_id):
        return self.rep_file.delete_by_id(customer_id)

    def get_count(self):
        return self.rep_file.get_count()
