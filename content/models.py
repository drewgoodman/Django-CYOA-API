from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.contrib.contenttypes.models import ContentType

from .utils.gamedata import *

# Create your models here.


class Campaign(models.Model):
    _id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=200, null=True, blank=True) # display name in main menu
    label = models.CharField(max_length=255, null=True, blank=True) #campaign file label for developer organization purposes
    description_short = models.TextField(null=True, blank=True) # short display description in main menu
    description_long = models.TextField(null=True, blank=True) # long display description before confirmation
    icon = models.ImageField(null=True, blank=True, default='/placeholder.png') # for main menu display
    feature_image = models.ImageField(null=True, blank=True, default='/placeholder.png') # for long description display / placeholder fallback image if scenes lack background images

    def __str__(self):
        return self.label

    def get_content_url(self):
        return reverse("content:view-campaign",kwargs={"slug":self._id})


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

    background_image = models.ImageField(null=True, blank=True, default='/placeholder.png') # display this image banner up top to set the scene described in text
    display_text = models.TextField() # text displayed on entering node --- can be formatted for special animations
    display_text_visited = models.TextField(null=True, blank=True) # optional; text to display if this is not the first time the player has visited this node

    def choices(self):
        return NodeChoice.objects.filter(scene_node_linked=self)

    def __str__(self):
        return self.label


class NodeChoice(models.Model): # an interactive option made available within a scene node
    _id = models.AutoField(primary_key=True, editable=False)
    label = models.CharField(max_length=255, null=True, blank=True) # file label for developer organization purposes
    scene_node_linked = models.ForeignKey(SceneNode, on_delete=models.SET_NULL, null=True)

    display_text = models.CharField(max_length=200, null=True, blank=True) # text to be displayed on choice button
    can_repeat = models.BooleanField(default=True) # if true, will appear every single time player visits the associated scene node

    has_condition = models.BooleanField(default=False) # if true, will only show node if the player meeds all conditions linked to this choice node
    can_fail = models.BooleanField(default=False) #if true, and the player fails to meet conditions; the player can still use this option, but it's a trap and will result in failure
    hide_on_condition_fail = models.BooleanField(default=True) # if true, and canFail is false, the node will NOT appear in the list at all if the player fails to meet the conditions. If false (and canFail is false as well), it will appear, but it will be grayed out instead and non-functional

    result_text = models.TextField(null=True, blank=True) # the text that displays when making the choice. Events are fired *after* this text displays
    result_text_on_fail = models.TextField(null=True, blank=True) # same as resultText, but plays if conditions are failed AND canFail is True --- is the result of a player making a choice and failing the check

    def __str__(self):
        return self.label + ": " + self.displayText


class ChoiceEvent(models.Model): # an event that fires after a choice is made and the resulting text displayed. Can be configured to fire on event failure as well
    _id = models.AutoField(primary_key=True, editable=False)
    type = models.CharField(max_length=20, choices=CONTENT_CONDITION_TYPES, blank=True)

    operator = models.CharField(null=True, blank=True, max_length=3, choices=CONTENT_PARAMS_OPERATORS, default='===')
    value = models.IntegerField(null=True, blank=True, default=0)

    call_on_failure = models.BooleanField(default=False) # call only if the player fails the conditions defined for a "successful" event
    position = models.IntegerField(default=0) # relative position to other events linked to same choice --- useful if order events are fired in matters

    def __str__(self):
        return self.type   


class Conditional(models.Model): # the "base" of a conditional check for a choice node -- must reference a ConditionType from utils.gameData, then optionally has a unqiue ConditionalOperator, ConditionalInteger, and/or ConditionalBoolean as needed
    _id = models.AutoField(primary_key=True, editable=False)
    type = models.CharField(max_length=20, choices=CONTENT_CONDITION_TYPES, blank=True)
    choice_linked = models.ForeignKey(Scene, on_delete=models.CASCADE, null=True)
    for_success = models.BooleanField(null=True, default=False) # if yes, then this condition is used to check whether the player can SUCCESSFULLY complete the choice option, not whether it shows up as an option in the first place

    #TODO: add position and AND/OR logic for more complex conditionals if needed in future

    def __str__(self):
        return self.type


class ConditionalOperator(models.Model): #one per conditional max
    condition = models.OneToOneField(Conditional, on_delete=models.CASCADE, primary_key=True)
    operator = models.CharField(null=True, blank=True, max_length=3, choices=CONTENT_PARAMS_OPERATORS, default='===')

    def __str__(self):
        return self.operator

class ConditionalBoolean(models.Model): #one per conditional max
    condition = models.OneToOneField(Conditional, on_delete=models.CASCADE, primary_key=True)
    value = models.BooleanField(default=True)

    def __str__(self):
        return self.value

class ConditionalInteger(models.Model): #one per conditional max
    condition = models.OneToOneField(Conditional, on_delete=models.CASCADE, primary_key=True)
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.value