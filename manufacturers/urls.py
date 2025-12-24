from django.urls import path
from . import views


urlpatterns = [
    path('manufacturers/', views.ManufacturersListCreateAPIView.as_view(), name='manufacturers-creat_list'),
    path('manufacturers/<int:pk>/', views.ManufacturersRetrieveUpdateDestroyAPIView.as_view(), name='manufacturers-detail-view'),
]
