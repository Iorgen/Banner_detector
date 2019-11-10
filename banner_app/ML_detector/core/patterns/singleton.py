class Singleton(type):
    """Чтобы сделать класс одиночкой -- укажите metaclass=Singleton

    Паттерн одиночка (Singleton)
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super().__call__(*args, **kwargs)
        return cls.__instances[cls]
