from django.urls import path
from . import views


urlpatterns = [
    path('drug/', views.DrugIdentificationListCreateAPIView.as_view(), name='drug-creat-list'),
    path('drug/<int:pk>/', views.DrugIdentificationRetrieveUpdateDestroyAPIView.as_view(), name='drug-detail-view'),
    path('drug/stats/', views.DrugIdentificationStatsView.as_view(), name='drug-stats-view'),
]
