from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.utils.safestring import mark_safe

from cloudinary.models import CloudinaryField

from ..utils.gamedata import *

# Create your models here.


class BackgroundImage(models.Model): #reference for background banners on scene nodes

    name = models.CharField(max_length=100)
    image = CloudinaryField(null=True, blank=True)

    def __str__(self):
        return self.name


class IconImage(models.Model): #reference for action-icon images

    name = models.CharField(max_length=100)
    image = CloudinaryField(null=True, blank=True)

    def __str__(self):
        return self.name