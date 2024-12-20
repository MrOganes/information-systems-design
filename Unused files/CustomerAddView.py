from datetime import datetime
from tkinter import Toplevel, Label, Entry, Button, messagebox

from Customer import Customer


class CustomerAddView:
    def __init__(self, add_customer_controller):
        self.add_customer_controller = add_customer_controller
        self.window = Toplevel()
        self.window.title("Добавить клиента")

        # Поля для ввода информации
        Label(self.window, text="Имя").grid(row=0, column=0)
        self.first_name_entry = Entry(self.window)
        self.first_name_entry.grid(row=0, column=1)

        Label(self.window, text="Фамилия").grid(row=1, column=0)
        self.last_name_entry = Entry(self.window)
        self.last_name_entry.grid(row=1, column=1)

        Label(self.window, text="Email").grid(row=2, column=0)
        self.email_entry = Entry(self.window)
        self.email_entry.grid(row=2, column=1)

        Label(self.window, text="Номер телефона", fg="grey").grid(row=3, column=0)
        self.phone_number_entry = Entry(self.window)
        self.phone_number_entry.grid(row=3, column=1)

        Label(self.window, text="Адрес", fg="grey").grid(row=4, column=0)
        self.address_entry = Entry(self.window)
        self.address_entry.grid(row=4, column=1)

        Label(self.window, text="Город", fg="grey").grid(row=5, column=0)
        self.city_entry = Entry(self.window)
        self.city_entry.grid(row=5, column=1)

        Label(self.window, text="Почтовый код", fg="grey").grid(row=6, column=0)
        self.postal_code_entry = Entry(self.window)
        self.postal_code_entry.grid(row=6, column=1)

        Label(self.window, text="Страна", fg="grey").grid(row=7, column=0)
        self.country_entry = Entry(self.window)
        self.country_entry.grid(row=7, column=1)

        # Кнопки
        Button(self.window, text="Добавить", command=self.add_customer).grid(row=8, column=0, columnspan=2)

    def add_customer(self):
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        phone_number = self.phone_number_entry.get()
        address = self.address_entry.get()
        city = self.city_entry.get()
        postal_code = self.postal_code_entry.get()
        country = self.country_entry.get()
        date_joined = datetime.now()
        try:
            customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                            address=address, city=city, postal_code=postal_code, country=country,
                            date_joined=date_joined)

            self.add_customer_controller.add_customer(customer)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")

    def destroy(self):
        self.window.destroy()
