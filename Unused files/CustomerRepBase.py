from ICustomerRepository import ICustomerRepository


class CustomerRepBase(ICustomerRepository):
    def __init__(self, strategy):
        self.strategy = strategy
        self.customers = strategy.read_all()

    def add_customer(self, customer):
        new_id = max([customer.get_customer_id() for customer in self.customers], default=0) + 1
        customer._set_id(new_id)

        if not self.__is_unique(customer.get_email()):
            raise ValueError("Customer with this email already exists.")

        self.customers.append(customer)
        self.strategy.save_all(self.customers)

    def get_by_id(self, customer_id):
        for customer in self.customers:
            if customer.get_customer_id() == customer_id:
                return customer
        raise ValueError(f"Customer with ID {customer_id} not found.")

    def get_k_n_short_list(self, k, n):
        start = (k - 1) * n
        end = start + n
        return self.customers[start:end]

    def replace_by_id(self, new_customer):
        if not self.__is_unique(new_customer.get_email(), new_customer.get_customer_id()):
            raise ValueError("Customer with this email already exists.")

        for i, customer in enumerate(self.customers):
            if customer.get_customer_id() == new_customer.get_customer_id():
                self.customers[i] = new_customer
                self.strategy.save_all(self.customers)
                return True
        return False

    def delete_by_id(self, customer_id):
        self.customers = [customer for customer in self.customers if customer.get_customer_id() != customer_id]
        self.strategy.save_all(self.customers)

    def get_count(self):
        return len(self.customers)

    def sort_by_field(self):
        self.customers.sort(key=lambda customer: customer.get_date_joined())

    # Проверка на уникальность email
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