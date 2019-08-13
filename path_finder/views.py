from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View


class RoutesView(View):
    def get(self, request):
        origin = self.kwargs.get('origin')
        destination = self.kwargs.get('destination')
        if (origin is None or destination is None):
            return HttpResponseBadRequest("Origin or Destination missing")
