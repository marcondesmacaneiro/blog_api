class StringHelper:

    def __init__(self, empty_string):
        self.string = empty_string

    @classmethod
    def non_empty_string(cls):
        if not cls:
            raise ValueError("Must not be empty string")
        return cls
