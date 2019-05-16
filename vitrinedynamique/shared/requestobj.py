from abc import ABC


class Request(ABC):
    pass


class InvalidRequest(Request):
    def __init__(self):
        self.errors = []

    def add_error(self, message):
        self.errors.append(message)

    def has_errors(self):
        return len(self.errors) > 0

    def __bool__(self):
        return False


class ValidRequest(Request):
    def __bool__(self):
        return True