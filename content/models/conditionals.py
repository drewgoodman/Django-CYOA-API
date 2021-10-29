from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType

from django.utils.safestring import mark_safe

from .images import BackgroundImage, IconImage
from .scenes import SceneNode, Scene
from ..utils.gamedata import *

class Conditional(models.Model): # the "base" of a conditional check for a choice node -- must reference a ConditionType from utils.gameData, then optionally has a unqiue ConditionalOperator, ConditionalInteger, and/or ConditionalBoolean as needed
    id = models.AutoField(primary_key=True, editable=False)
    type = models.CharField(max_length=20, choices=CONTENT_CONDITION_TYPES, blank=True)

    #TODO: add position and AND/OR logic for more complex conditionals if needed in future

    def __str__(self):
        return self.type


class ConditionalParam(models.Model): #generic class for all conditional param models
    condition = models.OneToOneField(Conditional, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        abstract = True


class ConditionalOperator(ConditionalParam): #one per conditional max
    operator = models.CharField(null=True, blank=True, max_length=3, choices=CONTENT_PARAMS_OPERATORS, default='===')

    def __str__(self):
        return self.operator


class ConditionalBoolean(ConditionalParam): #one per conditional max
    value = models.BooleanField(default=True)

    def __str__(self):
        return self.value


class ConditionalInteger(ConditionalParam): #one per conditional max
    value = models.IntegerField(default=0)

    def __str__(self):
        return self.value
