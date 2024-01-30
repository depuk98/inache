class CustomResponse():
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

    # def response(self):
    #     return JsonResponse({'message': self.message}, status=self.status_code)