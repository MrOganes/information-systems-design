class FileStrategy:
    def read_all(self):
        raise NotImplementedError("Метод должен быть реализован в конкретной стратегии")

    def save_all(self, customers):
        raise NotImplementedError("Метод должен быть реализован в конкретной стратегии")