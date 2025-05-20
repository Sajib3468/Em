from django.urls import path
from .views import EmployerListCreateAPIView, EmployerDetailAPIView

urlpatterns = [
    path('', EmployerListCreateAPIView.as_view(), name='employer-list-create'),
    path('<int:pk>/', EmployerDetailAPIView.as_view(), name='employer-detail'),
]
