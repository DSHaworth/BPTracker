from flask import jsonify

class ResponseHandler():
    """Generic Response Handler for valid and invalid responses"""
    def __init__(self, payload = None, errorMessage = None):
        self.isValid = not errorMessage
        self.errorMessage = errorMessage
        self.payload = payload

    def to_dict(self):
        return dict(
            isValid = self.isValid,
            errorMessage = self.errorMessage,
            payload = self.payload
        )
        #return jsonify(self) #.__dict__
        #return self.__dict__
