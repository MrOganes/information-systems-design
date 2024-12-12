import socketserver

from CustomerTableWeb import CustomerTableWeb
from CustomerController import CustomerController
from CustomerRepFileAdapter import CustomerRepFileAdapter
from JsonFileStrategy import JsonFileStrategy

# Параметры сервера
PORT = 8000

# Инициализация репозитория
repository = CustomerRepFileAdapter(JsonFileStrategy('Unused files/customers.json'))

# Инициализация контроллера
controller = CustomerController(repository)

customer_handler = CustomerTableWeb(controller)

# Запуск сервера
if __name__ == "__main__":
    with socketserver.TCPServer(("", PORT), customer_handler.get_handler()) as httpd:
        print(f"Server running at http://localhost:{PORT}")
        httpd.serve_forever()
