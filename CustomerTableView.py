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

        self.table = ttk.Treeview(self.table_frame, columns=('ID', 'First Name', 'Last Name', 'Email'), show='headings')
        self.table.heading('ID', text='ID')
        self.table.heading('First Name', text='First Name')
        self.table.heading('Last Name', text='Last Name')
        self.table.heading('Email', text='Email')

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

        # Размещаем кнопки в центре с помощью дополнительного Frame
        center_frame = tk.Frame(button_frame)
        center_frame.pack(side=tk.TOP, fill=tk.X)

        self.prev_button.pack(side=tk.LEFT, padx=5, expand=True)  # Кнопка слева
        self.next_button.pack(side=tk.LEFT, padx=5, expand=True)  # Кнопка справа
        self.add_button.pack(side=tk.RIGHT, padx=5, expand=True)  # Кнопка для добавления клиента

        # Загружаем данные при старте
        self.update_buttons()
        self.load_page(self.current_page)

    def update(self, customers):
        # Очистка таблицы перед обновлением
        for row in self.table.get_children():
            self.table.delete(row)

        # Заполнение таблицы
        for customer in customers:
            self.table.insert('', tk.END, values=(customer['customer_id'], customer['first_name'], customer['last_name'], customer['email']))

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
        add_controller = AddCustomerController(self)
        add_controller.show_add_window()

    def handle_error(self, error_message):
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {error_message}")

    def refresh_page(self):
        # Обновляем текущую страницу после добавления нового клиента
        self.load_page(self.current_page)
