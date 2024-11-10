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

    def add_customer(self):
        first_name = self.add_view.first_name_entry.get()
        last_name = self.add_view.last_name_entry.get()
        email = self.add_view.email_entry.get()
        phone_number = self.add_view.phone_number_entry.get()
        address = self.add_view.address_entry.get()
        city = self.add_view.city_entry.get()
        postal_code = self.add_view.postal_code_entry.get()
        country = self.add_view.country_entry.get()
        date_joined = datetime.datetime.now()

        try:
            new_customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                            address=address, city=city, postal_code=int(postal_code) if postal_code else None, country=country,
                            date_joined=date_joined)
        except Exception as e:
            messagebox.showerror("Ошибка", e)
            return

        try:
            self.repository.add_customer(new_customer)

            messagebox.showinfo("Успех", "Клиент успешно добавлен")
            self.add_view.destroy()

            self.parent_view.refresh_page()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")
