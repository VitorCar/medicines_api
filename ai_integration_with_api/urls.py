from django.urls import path
from . import views


urlpatterns = [
    path('ai/pharmacy/', views.SearchPharmacyAPIView.as_view(), name='ai-pharmacy'),
    path('ai/leaflet/', views.MedicineLeafletAPIView.as_view(), name='ai-leaflet'),
]
