from Observable import Observable


class CustomerController(Observable):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def load_customers(self, page, page_size):
        customers = self.repository.get_k_n_short_list(page, page_size)
        self.notify_observers(customers)
        return len(customers)
