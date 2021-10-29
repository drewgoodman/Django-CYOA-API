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
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # display name in main menu
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    description_short = models.TextField(null=True, blank=True) # short display description in main menu
    description_long = models.TextField(null=True, blank=True) # long display description before confirmation
    icon = models.ImageField(null=True, blank=True, default='/placeholder.png') # for main menu display
    feature_image = models.ForeignKey(BackgroundImage, on_delete=models.SET_NULL, null=True, blank=True) # for long description display / placeholder fallback image if scenes lack background images

    def __str__(self):
        return self.label

    def get_content_url(self):
        return reverse("content:view-campaign",kwargs={"slug":self.id})

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
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # location name to be displayed in-game
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    campaign_linked = models.ForeignKey(Campaign, on_delete=models.SET_NULL, null=True)

    objects = SceneManager()

    def nodes(self):
        return SceneNode.objects.filter(scene_linked=self)

    def __str__(self):
        return self.label

    def get_content_url(self):
        return reverse("content:scene-detail",kwargs={"slug":self.id,"campaign_id":self.campaign_linked.id})


class SceneNode(models.Model): # a traversable node inside the scene
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200) # location name to be displayed in-game
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    scene_linked = models.ForeignKey(Scene, on_delete=models.SET_NULL, null=True)
    background_image = models.ForeignKey(BackgroundImage, on_delete=models.SET_NULL, null=True, blank=True) # display this image banner up top to set the scene described in text
    display_text = models.TextField() # text displayed on entering node --- can be formatted for special animations
    display_text_visited = models.TextField(null=True, blank=True) # optional; text to display if this is not the first time the player has visited this node

    def choices(self):
        return NodeChoice.objects.filter(scene_node_linked=self)
    
    def background(self):
        if self.background_image:
            return self.background_image.image.url
        else:
            return 'https://via.placeholder.com/128'

    def __str__(self):
        if self.label:
            return self.label
        elif self.name:
            return self.name


class NodeChoice(models.Model): # an interactive option made available within a scene node

    id = models.AutoField(primary_key=True, editable=False)
    label = models.CharField(max_length=255, null=True, blank=True) # file label for developer organization purposes
    scene_node_linked = models.ForeignKey(SceneNode, on_delete=models.SET_NULL, null=True)
    icon_linked = models.ForeignKey(IconImage, on_delete=models.SET_NULL, null=True, blank=True) # icon displayed
    display_text = models.CharField(max_length=200, null=True, blank=True) # text to be displayed on choice button
    can_repeat = models.BooleanField(default=True) # if true, will appear every single time player visits the associated scene node
    has_condition = models.BooleanField(default=False) # if true, will only show node if the player meeds all conditions linked to this choice node
    can_fail = models.BooleanField(default=False) #if true, and the player fails to meet conditions; the player can still use this option, but it's a trap and will result in failure
    hide_on_condition_fail = models.BooleanField(default=True) # if true, and canFail is false, the node will NOT appear in the list at all if the player fails to meet the conditions. If false (and canFail is false as well), it will appear, but it will be grayed out instead and non-functional
    result_text = models.TextField(null=True, blank=True) # the text that displays when making the choice. Events are fired *after* this text displays
    result_text_on_fail = models.TextField(null=True, blank=True) # same as resultText, but plays if conditions are failed AND canFail is True --- is the result of a player making a choice and failing the check

    def __str__(self):
        return self.label + ": " + self.display_text
    
    def icon(self):
        if self.icon_linked:
            return self.icon_linked.image.url
        else:
            return 'https://via.placeholder.com/128'
