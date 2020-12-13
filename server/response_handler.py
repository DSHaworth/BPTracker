from flask import jsonify

class ResponseHandler():
    """Generic Response Handler for valid and invalid responses"""
    def __init__(self, payload = None, errorMessage = None):
        self.payload = payload        
        self.errorMessage = errorMessage
        self.isValid = not errorMessage

    def jsonify(self):
        return jsonify(dict(
            isValid = self.isValid,
            errorMessage = self.errorMessage,
            payload = self.payload
        ))
        #return jsonify(self) #.__dict__
        #return self.__dict__
