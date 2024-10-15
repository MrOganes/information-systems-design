class Observable:
    def __init__(self):
        self.__observers = []

    def add_observer(self, observer):
        self.__observers.append(observer)

    def notify_observers(self, data):
        for observer in self.__observers:
            observer.update(data)
