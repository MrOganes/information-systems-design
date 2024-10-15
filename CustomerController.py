from Observable import Observable


class CustomerController(Observable):
    def __init__(self, repository):
        super().__init__()
        self.repository = repository

    def load_customers(self, page, page_size):
        try:
            customers = self.repository.get_k_n_short_list(page, page_size)
            self.notify_observers(customers)
            return len(customers)
        except Exception as e:
            self.notify_observers_error(str(e))
            return 0

    def notify_observers_error(self, error_message):
        for observer in self._Observable__observers:
            observer.handle_error(error_message)
