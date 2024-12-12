from Customer import Customer
from DatabaseConnection import DatabaseConnection


class CustomerRepPostgres:
    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        self.db = DatabaseConnection(db_name, user, password, host, port)

    def add_customer(self, customer):
        query = """
            INSERT INTO customers (first_name, last_name, email, phone_number, address, city, postal_code, country, date_joined)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING customer_id
        """
        data = customer.to_dict()
        self.db.execute(query, (data['first_name'], data['last_name'], data['email'], data['phone_number'],
                                data['address'], data['city'], data['postal_code'], data['country'],
                                data['date_joined']))
        new_id = self.db.fetchone()[0]
        self.db.commit()

    # Получить объект по ID
    def get_by_id(self, customer_id):
        query = "SELECT * FROM customers WHERE customer_id = %s"
        self.db.execute(query, (customer_id,))
        data = self.db.fetchone()
        if data:
            return Customer(customer_id=data.get('customer_id'),
                            first_name=data['first_name'],
                            last_name=data['last_name'],
                            email=data['email'],
                            phone_number=data.get('phone_number'),
                            address=data.get('address'),
                            city=data.get('city'),
                            postal_code=data.get('postal_code'),
                            country=data.get('country'),
                            date_joined=data.get('date_joined'))
        return None

    def get_k_n_short_list(self, k, n):
        offset = (k - 1) * n
        query = "SELECT * FROM customers ORDER BY customer_id LIMIT %s OFFSET %s"
        self.db.execute(query, (n, offset))
        return self.db.fetchall()

    def replace_by_id(self, new_customer):
        query = """
            UPDATE customers 
            SET first_name = %s, last_name = %s, email = %s, phone_number = %s, address = %s, city = %s, postal_code = %s, country = %s, date_joined = %s
            WHERE customer_id = %s
        """
        data = new_customer.to_dict()
        self.db.execute(query, (data.get('first_name'), data.get('last_name'), data.get('email'), data.get('phone_number'),
                                data.get('address'), data.get('city'), data.get('postal_code'), data.get('country'),
                                data.get('date_joined'), data.get('customer_id')))
        self.db.commit()

    def delete_by_id(self, customer_id):
        query = "DELETE FROM customers WHERE customer_id = %s"
        self.db.execute(query, (customer_id,))
        self.db.commit()

    def get_count(self):
        query = "SELECT COUNT(*) FROM customers"
        self.db.execute(query)
        return self.db.fetchone()[0]
