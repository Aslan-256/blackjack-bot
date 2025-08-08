class Card:
    def __init__(self, value: int):
        self.__value = value


    def get_value(self):
        return self.__value

    def __repr__(self):
        return f"{self.__value}"