from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from django.utils.safestring import mark_safe

from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField

from .images import BackgroundImage, IconImage
from ..utils.gamedata import *

# Create your models here.

class Campaign(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # display name in main menu
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    description_short = models.TextField(null=True, blank=True) # short display description in main menu
    description_long = models.TextField(null=True, blank=True) # long display description before confirmation
    icon = models.ImageField(null=True, blank=True, default='/placeholder.png') # for main menu display
    feature_image = models.ForeignKey(BackgroundImage, on_delete=models.SET_NULL, null=True, blank=True) # for long description display / placeholder fallback image if scenes lack background images

    def __str__(self):
        return self.label

    def get_content_url(self):
        return reverse("content:view-campaign",kwargs={"slug":self._id})

    def get_image_url(self):
        if self.feature_image:
            return self.feature_image.image.url
        else:
            return "/placeholder.png"
    
    def get_background_image(self):
        return mark_safe(CloudinaryImage(self.feature_image.image.url).image(secure=True, transformation=[
        {'width':150, 'height': 150}
        ]))

class SceneManager(models.Manager):

    def filter_by_campaign(self, instance):
        # queryset = Scene.objects.filter(campaignLinked=instance)
        queryset = super(SceneManager, self).filter(campaign_linked=instance)
        return queryset


class Scene(models.Model): #hosts a cluster of traversable nodes / largely for organization purposes. can also give overhead GPS location data to player
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # location name to be displayed in-game
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    campaign_linked = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)

    objects = SceneManager()

    def nodes(self):
        return SceneNode.objects.filter(scene_linked=self)

    def __str__(self):
        return self.label

    def get_content_url(self):
        return reverse("content:scene-detail",kwargs={"slug":self._id,"campaign_id":self.campaign_linked._id})


class SceneNode(models.Model): # a traversable node inside the scene
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # location name to be displayed in-game
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    scene_linked = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True)
    background_image = models.ForeignKey(BackgroundImage, on_delete=models.SET_NULL, null=True, blank=True) # display this image banner up top to set the scene described in text
    display_text = models.TextField() # text displayed on entering node --- can be formatted for special animations
    display_text_visited = models.TextField(null=True, blank=True) # optional; text to display if this is not the first time the player has visited this node

    def choices(self):
        return NodeChoice.objects.filter(scene_node_linked=self)

    def __str__(self):
        return self.label