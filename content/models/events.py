from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from django.utils.safestring import mark_safe

from cloudinary import CloudinaryImage
from cloudinary.models import CloudinaryField

from .images import BackgroundImage, IconImage
from .scenes import SceneNode, Scene
from ..utils.gamedata import *

# Create your models here.


class ChoiceEvent(models.Model): # an event that fires after a choice is made and the resulting text displayed. Can be configured to fire on event failure as well

    id = models.AutoField(primary_key=True, editable=False)
    type = models.CharField(max_length=20, choices=CONTENT_CONDITION_TYPES, blank=True)
    operator = models.CharField(null=True, blank=True, max_length=3, choices=CONTENT_PARAMS_OPERATORS, default='===')
    value = models.IntegerField(null=True, blank=True, default=0)
    call_on_failure = models.BooleanField(default=False) # call only if the player fails the conditions defined for a "successful" event
    position = models.IntegerField(default=0) # relative position to other events linked to same choice --- useful if order events are fired in matters

    def __str__(self):
        return self.type   

