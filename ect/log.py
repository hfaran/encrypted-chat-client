def log(func, self, method, message):
    try:
        func("{}.{}: {}".format(self.__class__.__name__, method.__name__,
                               message))
    except AttributeError:
        func("{}.{}: {}".format(self, method.__name__, message))
