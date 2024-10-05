from CustomerRepPostgres import CustomerRepPostgres
from ICustomerRepository import ICustomerRepository


class CustomerRepPostgresAdapter(ICustomerRepository):
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.rep_postgres = CustomerRepPostgres(db_name, user, password, host, port)

    def add_customer(self, customer):
        return self.rep_postgres.add_customer(customer)

    def get_by_id(self, customer_id):
        return self.rep_postgres.get_by_id(customer_id)

    def get_k_n_short_list(self, k, n):
        return self.rep_postgres.get_k_n_short_list(k, n)

    def replace_by_id(self, new_customer):
        return self.rep_postgres.replace_by_id(new_customer)

    def delete_by_id(self, customer_id):
        return self.rep_postgres.delete_by_id(customer_id)

    def get_count(self):
        return self.rep_postgres.get_count()