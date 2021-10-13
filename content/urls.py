from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_view, name='login'),
    path('campaign/create', views.create_campaign, name='create-campaign'),
    path('campaign/<slug>', views.view_campaign, name='view-campaign'),
]