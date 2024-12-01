import datetime
import json
import urllib
from http.server import SimpleHTTPRequestHandler

from AddCustomerController import AddCustomerController
from Customer import Customer

class CustomerTableWeb(SimpleHTTPRequestHandler):
    """Обработчик запросов для API и статических файлов."""

    def __init__(self, controller):
        self.controller = controller
        self.page = 1

    class CustomerTableWebWithController(SimpleHTTPRequestHandler):
        """Обертка для работы с переданным контроллером."""

        def __init__(self, *args, **kwargs):
            self.custom_handler = kwargs.pop("custom_handler")
            super().__init__(*args, **kwargs)

        def do_GET(self):
            parsed_path = urllib.parse.urlparse(self.path)

            if parsed_path.path == "/customers":
                # Получение списка клиентов
                query = urllib.parse.parse_qs(parsed_path.query)
                page = int(query.get("page", [1])[0])
                self.custom_handler.page = page
                page_size = int(query.get("page_size", [10])[0])

                # Загрузка клиентов
                customers = self.custom_handler.controller.load_customers(page, page_size)

                # Вычисляем флаги для кнопок
                has_prev = page > 1
                has_next = len(customers) >= page_size

                # Формируем ответ
                response = {
                    "customers": [customer.to_dict() for customer in customers],
                    "has_prev": has_prev,
                    "has_next": has_next,
                }
                self._send_response(200, response)
            elif parsed_path.path.startswith('/customer/'):
                customer_id = int(self.path.split("/")[-1])

                customer = self.custom_handler.controller.get_customer_by_id(customer_id)
                if customer:
                    self._send_response(200, customer.to_dict())
                else:
                    self._send_response(404, {"error": "Customer not found"})
            else:
                # Отправка статических файлов
                super().do_GET()

        def do_POST(self):
            add_controller = AddCustomerController(self, self.custom_handler.controller.repository)
            if self.path == "/add_customer":
                # Добавление клиента
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                customer_data = json.loads(post_data)
                try:
                    customer = Customer(first_name=customer_data.get('first_name'), last_name=customer_data.get('last_name'),
                                    email=customer_data.get('email'), phone_number=customer_data.get('phone_number'),
                                    address=customer_data.get('address'), city=customer_data.get('city'),
                                    postal_code=customer_data.get('postal_code'), country=customer_data.get('country'),
                                    date_joined=datetime.datetime.now())
                    add_controller.add_customer(customer)
                except Exception as e:
                    self._send_response(400, {"error": str(e)})
                else:
                    self._send_response(201, {"message": "Customer added successfully"})

            elif self.path.startswith('/update_customer/'):
                # Изменение клиента
                customer_id = int(self.path.split("/")[-1])

                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                customer_data = json.loads(post_data)

                try:
                    customer = Customer(first_name=customer_data.get('first_name'), last_name=customer_data.get('last_name'),
                                    email=customer_data.get('email'), phone_number=customer_data.get('phone_number'),
                                    address=customer_data.get('address'), city=customer_data.get('city'),
                                    postal_code=customer_data.get('postal_code'), country=customer_data.get('country'),
                                    date_joined=customer_data.get('date_joined'), customer_id=customer_id)

                    add_controller.replace_by_id(customer)
                except Exception as e:
                    self._send_response(400, {"error": str(e)})
                else:
                    self._send_response(201, {"message": "Customer update successfully"})

        def _send_response(self, status_code, data):
            """Формирование HTTP-ответа."""
            self.send_response(status_code)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode("utf-8"))

    def get_handler(self):
        """Возвращает обработчик с подключённым контроллером."""
        def handler(*args, **kwargs):
            self.CustomerTableWebWithController(custom_handler=self, *args, **kwargs)
        return handler
