import datetime
from tkinter import Toplevel, Label, Entry, Button
from tkinter import messagebox
from Customer import Customer


class AddCustomerController:
    def __init__(self, parent_view):
        self.parent_view = parent_view
        self.window = None

    def show_add_window(self):
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
        date_joined = datetime.datetime.now()

        try:
            new_customer = Customer(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                            address=address, city=city, postal_code=int(postal_code), country=country,
                            date_joined=date_joined)
        except Exception as e:
            messagebox.showerror("Ошибка", e)
            return

        try:
            self.parent_view.controller.repository.add_customer(new_customer)

            messagebox.showinfo("Успех", "Клиент успешно добавлен")
            self.window.destroy()

            self.parent_view.refresh_page()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось добавить клиента: {e}")
