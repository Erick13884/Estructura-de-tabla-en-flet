class ApiError(Exception):
    def __init__(self, message, status_code=0):
        self.message = message
        self.status_code = status_code

def api_error_to_text(error):
    return str(error)