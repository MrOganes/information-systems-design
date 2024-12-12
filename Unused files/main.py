import tkinter as tk

from CustomerController import CustomerController
from CustomerRepFileAdapter import CustomerRepFileAdapter
from CustomerRepPostgres import CustomerRepPostgres
from CustomerTableView import CustomerTableView
from JsonFileStrategy import JsonFileStrategy

if __name__ == "__main__":
    # Инициализация репозитория
    # repository = CustomerRepPostgres(db_name="postgres", user="postgres", password="357951")
    repository = CustomerRepFileAdapter(JsonFileStrategy('customers.json'))

    # Инициализация контроллера
    controller = CustomerController(repository)

    # Инициализация GUI
    root = tk.Tk()
    view = CustomerTableView(root, controller)

    # Запуск GUI
    root.mainloop()
