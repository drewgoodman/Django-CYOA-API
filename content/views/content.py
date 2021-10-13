from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages


from ..forms import UserLoginForm
from ..models import *

def view_campaign(request, slug=None):
    instance = get_object_or_404(Campaign, _id=slug)
    scenes = Scene.objects.filter_by_campaign(instance)
    context = {
        "name": instance.name,
        "description_long": instance.description_long,
        "scenes": scenes
    }
    return render(request, 'content/campaign_detail.html', context)