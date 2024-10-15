import tkinter as tk

from CustomerController import CustomerController
from CustomerRepPostgres import CustomerRepPostgres
from CustomerTableView import CustomerTableView

if __name__ == "__main__":
    # Инициализация репозитория
    repository = CustomerRepPostgres(db_name="postgres", user="postgres", password="357951")

    # Инициализация контроллера
    controller = CustomerController(repository)

    # Инициализация GUI
    root = tk.Tk()
    view = CustomerTableView(root, controller)

    # Запуск GUI
    root.mainloop()
