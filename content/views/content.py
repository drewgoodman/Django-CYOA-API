from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages


from ..forms import CampaignForm, SceneForm, SceneNodeForm
from ..models import *

def view_campaign(request, slug=None):
    instance = get_object_or_404(Campaign, _id=slug)
    scenes = Scene.objects.filter_by_campaign(instance)
    context = {
        "name": instance.name,
        "campaign_id": instance._id,
        "description_long": instance.description_long,
        "scenes": scenes
    }
    return render(request, 'content/campaign_detail.html', context)

def create_campaign(request):
    if not request.user.is_authenticated:
        raise Http404

    form = CampaignForm(request.POST or None, request.FILES or None)
    if form.is_valid() and request.user.is_authenticated:
        instance = form.save(commit=False)
        try:
            feature_image = request.FILES['file']
        except:
            feature_image = None
        if feature_image:
            instance.feature_image = feature_image
        instance.save()
        return HttpResponseRedirect(instance.get_content_url())

    context = {
        "form": form
    }
    return render(request, 'content/campaign_create.html', context)

def create_scene(request, slug=None):
    if not request.user.is_authenticated:
        raise Http404
    instance = get_object_or_404(Campaign, _id=slug)
    initial_data = {
        "campaign_linked": instance
    }
    form = SceneForm(request.POST or None, request.FILES or None, initial=initial_data)
    if form.is_valid() and request.user.is_authenticated:
        instance = form.save(commit=False)
        # try:
        #     feature_image = request.FILES['file']
        # except:
        #     feature_image = None
        # if feature_image:
        #     instance.feature_image = feature_image
        instance.save()
    context = {
        "form": form
    }
    return render(request, 'content/scene_create.html', context)

def scene_detail(request, slug=None, campaign_id=None):
    instance = get_object_or_404(Scene, _id=slug)
    context = {
        "scene": instance
    }
    return render(request, 'content/scene_detail.html', context)