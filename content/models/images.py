from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.utils.safestring import mark_safe

from cloudinary.models import CloudinaryField

from ..utils.gamedata import *

# Create your models here.


class BackgroundImage(models.Model): #reference for background banners on scene nodes

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    image = CloudinaryField('image', null=True, blank=True)
    description_short = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class IconImage(models.Model): #reference for action-icon images

    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    image = CloudinaryField(null=True, blank=True)
    description_short = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name