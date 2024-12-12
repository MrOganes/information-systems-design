from Observable import Observable


class CustomerController(Observable):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def load_customers(self, page, page_size):
        try:
            customers = self.repository.get_k_n_short_list(page, page_size)
            self.notify_observers(customers)
            return customers
        except Exception as e:
            self.notify_observers_error(str(e))
            return []

    def remove_customer(self, customer_id):
        try:
            self.repository.delete_by_id(customer_id)
        except Exception as e:
            self.notify_observers_error(str(e))

    def notify_observers_error(self, error_message):
        for observer in self._Observable__observers:
            observer.handle_error(error_message)

    def get_customer_by_id(self, customer_id):
        try:
            customer = self.repository.get_by_id(customer_id)
            return customer
        except Exception as e:
            self.notify_observers_error(str(e))
            return None
