from django.urls import path
from . import views

app_name = "content"

urlpatterns = [
    path('', views.home, name="home"),
    path('login', views.login_view, name='login'),
    path('campaign/create', views.create_campaign, name='create-campaign'),
    path('images/upload', views.upload_image, name='upload-image'),
    path('campaign/<slug>/scenes/create', views.create_scene, name='create-scene'),
    path('campaign/<campaign_id>/scenes/<slug>', views.scene_detail, name='scene-detail'),
    path('campaign/<slug>', views.view_campaign, name='view-campaign'),
]