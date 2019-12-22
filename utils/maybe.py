class Maybe:

    def __init__(self, value):
        self.__is_just = value is not None
        self.__value = value

    def is_nothing(self):
        return not self.__is_just

    def is_just(self):
        return self.__is_just

    def map(self, f):
        if self.is_just():
            new_value = f(self.__value)
            return self.just(new_value)
        else:
            return self.nothing()

    def flat_map(self, f):
        if self.is_just():
            new_value = f(self.__value)
            if isinstance(new_value, Maybe):
                return self.just(new_value.__value)
            return new_value
        else:
            return self.nothing()

    def get(self):
        return self.__value

    def if_present(self, f):
        if self.is_just():
            f(self.__value)

    def if_present_or_else(self, f, g):
        if self.is_just():
            f(self.__value)
        else:
            g()

    def or_else(self, y):
        if self.is_just():
            return self.__value
        else:
            return y

    def or_else_get(self, f):
        if self.is_just():
            return self.__value
        else:
            return f()

    @staticmethod
    def nothing():
        return Maybe(None)

    @staticmethod
    def just(x):
        return Maybe(x)
