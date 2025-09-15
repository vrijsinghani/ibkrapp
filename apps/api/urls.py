from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.api.views import SalesListCreateView, SalesDetailView

urlpatterns = [
    path("sales/", csrf_exempt(SalesListCreateView.as_view())),
    path("sales/<int:pk>/", csrf_exempt(SalesDetailView.as_view())),
]