from django.urls import path
from . import views


urlpatterns = [
    path('administration/', views.RoutesOfAdministrationListCreateAPIView.as_view(), name='Administration-creat-list'),
    path('administration/<int:pk>/',
         views.RoutesOfAdministrationRetrieveUpdateDestroyAPIView.as_view(),
         name='Administration-detail-view'),
]
