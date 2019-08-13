from django.urls import path
from path_finder.views import RoutesView

urlpatterns = [
    path('find_route', RoutesView.as_view())
]
