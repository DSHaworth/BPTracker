class Response_Handler():
    """Generic Response Handler for valid and invalid responses"""
    def __init__(self, payload = None, errorMessage = None):
        self.isValid = not errorMessage
        self.errorMessage = errorMessage
        self.payload = payload

    def to_JSON(self):
        return self.__dict__
