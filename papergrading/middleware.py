# myapp/middleware.py

from .models import MarkSheet

# clearing the table after the exiting the page
class ClearDataMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Check if the session variable is set
        if 'data_displayed' in request.session:
            # Delete the data from the database
            MarkSheet.objects.all().delete()
            # Remove the session variable
            del request.session['data_displayed']
        print("cleared")

        return response
