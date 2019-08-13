from django.http import HttpResponse, HttpResponseBadRequest
from django.views import View
from path_finder.utility.PathSearch import PathSearcher
from django.views.decorators.csrf import csrf_exempt


class RoutesView(View):

    @csrf_exempt
    def get(self, request):
        origin = self.request.GET.get('origin')
        destination = self.request.GET.get('destination')
        if (origin is None or destination is None):
            return HttpResponseBadRequest(
                "Origin or Destination parameters are missing")

        searcher = PathSearcher()
        searcher.build_graph(origin, destination)
        path = searcher.find_shortest_path(origin, destination)

        errors = searcher.errors()
        if errors:
            return HttpResponseBadRequest(errors[0])

        return HttpResponse(self.formatted_path(path))

    def formatted_path(self, path):

        route = ""
        for i, airport in enumerate(path):
            if (i == 0):
                route += airport
            else:
                route += f' -> {airport}'

        return route
