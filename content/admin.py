from django.contrib import admin
from .models import BackgroundImage, IconImage, Campaign, Scene, SceneNode, NodeChoice, ChoiceEvent, Conditional, ConditionalBoolean, ConditionalInteger, ConditionalOperator

# Register your models here.

admin.site.register(BackgroundImage)
admin.site.register(IconImage)

admin.site.register(Campaign)

admin.site.register(Scene)
admin.site.register(SceneNode)

admin.site.register(NodeChoice)
admin.site.register(ChoiceEvent)

admin.site.register(Conditional)
admin.site.register(ConditionalOperator)
admin.site.register(ConditionalBoolean)
admin.site.register(ConditionalInteger)