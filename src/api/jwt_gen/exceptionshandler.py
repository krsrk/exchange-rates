class UnsupportedAlgoException(Exception):
    message = ''

    def __init__(self, message="Unsupported JWT Algo"):
        super().__init__(self.message)


class InvalidDataForRS256AlgoException(Exception):
    message = ''

    def __init__(self, message="Invalid data for JWT Algo RS256"):
        super().__init__(self.message)