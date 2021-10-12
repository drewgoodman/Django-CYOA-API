from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Campaign)

admin.site.register(Scene)
admin.site.register(SceneNode)

admin.site.register(NodeChoice)
admin.site.register(ChoiceEvent)

admin.site.register(Conditional)
admin.site.register(ConditionalOperator)
admin.site.register(ConditionalBoolean)
admin.site.register(ConditionalInteger)