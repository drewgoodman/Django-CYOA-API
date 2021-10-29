from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model
)
from django.utils.translation import gettext_lazy as _

from content.models import Campaign, Scene, SceneNode, NodeChoice

User = get_user_model()

<<<<<<< HEAD
=======
class BackgroundImageForm(forms.ModelForm):
    image = CloudinaryFileField(
        options = {
            'tags': "CYOA, background image, zcoast, upload",
            'crop': "limit", "width": 1920, "height": 1080,
            'folder': 'zcoast/background-image',
            'overwrite': True
        }
    )
    class Meta:
        model = BackgroundImage
        fields = '__all__'


class IconImageForm(forms.ModelForm):
    image = CloudinaryFileField(
        options = {
            'tags': "CYOA, icon, zcoast, upload",
            'crop': "limit", "width": 512, "height": 512,
            'folder': 'zcoast/icons',
            'overwrite': True
        }
    )
    class Meta:
        model = IconImage
        fields = '__all__'

>>>>>>> cloud-static

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This user does not exist.")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password.")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active.")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = (
            "name",
            "label",
            "feature_image",
            "description_short",
            "description_long",
        )
        labels = {
            "name": _('Campaign Title'),
            "label": _('Development Label (not visible to players)'),
            "feature_image": _('Featured Image'),
            "description_short": _('Short main menu description'),
            "description_long": _('Longer campaign summary')
        }


class SceneForm(forms.ModelForm):
    class Meta:
        model = Scene
        fields = (
            "name",
            "label",
        )
        labels = {
            "name": _('Scene Title'),
            "label": _('Development Label (not visible to players)'),
        }


class SceneNodeForm(forms.ModelForm):
    class Meta:
        model = SceneNode
        fields = (
            "name",
            "label",
            "background_image",
            "display_text",
            "display_text_visited",
        )
        labels = {
            "name": _('Scene Title'),
            "label": _('Development Label (not visible to players)'),
            "display_text": _('Text displayed on entering node'),
            "display_text_visited": _('Alternate text that can be displayed when revisiting the node')
        }


class NodeChoiceForm(forms.ModelForm):
    class Meta:
        model = NodeChoice
        fields = (
            "label",
            "display_text",
            "result_text",
            "can_repeat",
            "has_condition",
            "hide_on_condition_fail",
            "can_fail",
            "result_text_on_fail",
        )
        labels = {
            "label": _('Development Label (not visible to players)'),
            "display_text": _('Text to be displayed to player'),
            "result_text": _('Result text from successful choice'),
            "can_repeat": _('Can be repeated multiple times?'),
            "has_condition": _('Has conditions for success?'),
            "hide_on_condition_fail": _("Hide this choice if condition isn't met?"),
            "can_fail": _('Can it be chosen and result in failure?'),
            "result_text_on_fail": _('Result text on failure')
        }