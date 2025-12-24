from django.urls import path
from . import views


urlpatterns = [
    path('pharmaceutical/', views.PharmaceuticalFormsListCreateApiView.as_view(), name='pharmaceutical-creat-list'),
    path('pharmaceutical/<int:pk>/',
         views.PharmaceuticalFormsRetrieveUpdateDestroyAPIView.as_view(),
         name='pharmaceutical-detail-view'),
]
