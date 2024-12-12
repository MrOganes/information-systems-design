import datetime

from tkinter import messagebox
from Customer import Customer
from CustomerAddView import CustomerAddView


class AddCustomerController:
    def __init__(self, parent_view,  repository):
        self.repository = repository
        self.parent_view = parent_view
        self.window = None

    def show_add_window(self):
        self.add_view = CustomerAddView(self)

    def add_customer(self, new_customer):

        try:
            self.repository.add_customer(new_customer)

            messagebox.showinfo("Успех", "Клиент успешно добавлен")
            self.add_view.destroy()

            self.parent_view.refresh_page()
        except Exception as e:
            raise ValueError(str(e))

    def replace_by_id(self, customer):
        try:
            self.repository.add_customer(customer)
        except Exception as e:
            raise ValueError(str(e))

