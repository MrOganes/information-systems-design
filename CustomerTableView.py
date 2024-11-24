import tkinter as tk
from tkinter import ttk, messagebox
from AddCustomerController import AddCustomerController


class CustomerTableView:
    def __init__(self, root, controller):
        self.controller = controller
        self.controller.add_observer(self)

        # Переменные для отслеживания текущей страницы
        self.current_page = 1
        self.page_size = 10

        # Интерфейс окна
        self.root = root
        self.root.title("Customer Management")
        self.root.geometry("850x400")  # Размер окна
        self.root.resizable(False, False)  # Запрет изменения размера окна

        # Минимальные настройки стиля для сдержанности
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("Arial", 10), foreground="black", background="#F5F5F5")
        style.configure("Treeview", rowheight=25, font=("Arial", 9))

        # Таблица
        self.table_frame = tk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.table = ttk.Treeview(self.table_frame, columns=('ID', '№', 'First Name', 'Last Name', 'Email'), show='headings')
        self.table.heading('№', text='№')
        self.table.heading('First Name', text='First Name')
        self.table.heading('Last Name', text='Last Name')
        self.table.heading('Email', text='Email')

        self.table.column('ID', width=0, stretch=tk.NO)
        self.table.pack(fill=tk.BOTH, expand=True)

        # Frame для кнопок
        button_frame = tk.Frame(root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)

        # Обычный стиль для кнопок — без ярких акцентов
        button_style = {
            "bg": "#E0E0E0", "fg": "black", "font": ("Arial", 9),
            "activebackground": "#D3D3D3", "bd": 1, "relief": tk.RAISED,
            "width": 15, "height": 1
        }

        # Создаем кнопки
        self.prev_button = tk.Button(button_frame, text="Предыдущие 10", command=self.load_previous, **button_style)
        self.next_button = tk.Button(button_frame, text="Следующие 10", command=self.load_next, **button_style)
        self.add_button = tk.Button(button_frame, text="Добавить клиента", command=self.open_add_customer_window, **button_style)
        self.del_button = tk.Button(button_frame, text="Удалить клиента", command=self.remove_customer,
                                    **button_style)
        self.view_button = tk.Button(button_frame, text="Подробнее", command=self.view_customer_details, **button_style)

        center_frame = tk.Frame(button_frame)
        center_frame.pack(side=tk.TOP, fill=tk.X)

        self.prev_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.next_button.pack(side=tk.LEFT, padx=5, expand=True)
        self.add_button.pack(side=tk.RIGHT, padx=5, expand=True)
        self.del_button.pack(side=tk.RIGHT, padx=5, expand=True)
        self.view_button.pack(side=tk.LEFT, padx=5, expand=True)

        # Загружаем данные при старте
        self.update_buttons()
        self.load_page(self.current_page)

    def update(self, customers):
        # Очистка таблицы перед обновлением
        for row in self.table.get_children():
            self.table.delete(row)

        # Заполнение таблицы
        for i, customer in enumerate(customers):
            self.table.insert('', tk.END, values=(customer.get_customer_id(), (self.current_page - 1)*10+i+1, customer.get_first_name(),
                                                  customer.get_last_name(), customer.get_email()))

    def load_page(self, page):
        # Загрузка страницы данных
        loaded_count = self.controller.load_customers(page, self.page_size)
        self.update_buttons(loaded_count)

    def load_previous(self):
        # Загрузка предыдущей страницы
        if self.current_page > 1:
            self.current_page -= 1
            self.load_page(self.current_page)

    def load_next(self):
        # Загрузка следующей страницы
        self.current_page += 1
        self.load_page(self.current_page)

    def remove_customer(self):
        selected_items = self.table.selection()

        if not selected_items:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите клиента для удаления.")
            return

        for item in selected_items:
            customer_id = self.table.item(item, "values")[0]
            self.controller.remove_customer(int(customer_id))

        self.refresh_page()

    def update_buttons(self, loaded_count=None):
        # Обновление состояния кнопок

        # Отключаем кнопку "Предыдущие 10", если мы на первой странице
        if self.current_page == 1:
            self.prev_button.config(state=tk.DISABLED)
        else:
            self.prev_button.config(state=tk.NORMAL)

        # Отключаем кнопку "Следующие 10", если загружено меньше записей, чем page_siz
        if loaded_count is not None and loaded_count < self.page_size:
            self.next_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)

    def open_add_customer_window(self):
        # Открываем окно добавления клиента через контроллер
        add_controller = AddCustomerController(self, self.controller.repository)
        add_controller.show_add_window()

    def handle_error(self, error_message):
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {error_message}")

    def refresh_page(self):
        self.load_page(self.current_page)

    def view_customer_details(self):
        # Получаем ID выбранного клиента
        selected_items = self.table.selection()
        if not selected_items:
            messagebox.showwarning("Внимание", "Пожалуйста, выберите клиента для просмотра.")
            return

        # Получаем ID клиента
        customer_id = self.table.item(selected_items[0], "values")[0]
        customer = self.controller.get_customer_by_id(int(customer_id))

        if customer:
            self.open_customer_details_window(customer)
        else:
            messagebox.showwarning("Ошибка", "Не удалось загрузить информацию о клиенте.")

    def open_customer_details_window(self, customer):
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Подробная информация о клиенте {customer.get_first_name()} {customer.get_last_name()}")

        # Размещение информации в окне
        tk.Label(details_window, text=f"ID: {customer.get_customer_id()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Имя: {customer.get_first_name()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Фамилия: {customer.get_last_name()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Email: {customer.get_email()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Телефон: {customer.get_phone_number()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Адрес: {customer.get_address()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Город: {customer.get_city()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Почтовый код: {customer.get_postal_code()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Страна: {customer.get_country()}", anchor='w').pack(padx=10, pady=5, fill='x')
        tk.Label(details_window, text=f"Дата добавления: {customer.get_date_joined()}", anchor='w').pack(padx=10, pady=5, fill='x')

        # Добавляем кнопку для закрытия окна
        close_button = tk.Button(details_window, text="Закрыть", command=details_window.destroy)
        close_button.pack(pady=10)
