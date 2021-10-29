from django.urls import path
from . import views


urlpatterns = [
    path('campaign/<str:pk>/',views.campaign_data, name='campaign-data'),
    path('campaign/',views.campaign_list, name='campaign-list'),
    path('',views.api_overview, name="api-overview"),
]