from rest_framework import serializers
from content.models import Campaign, Scene, SceneNode, NodeChoice

class CampaignSerializer(serializers.ModelSerializer):

    image_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.feature_image:
            return obj.feature_image.image.url
        else:
            return ""


class CampaignDataSerializer(CampaignSerializer):

    scenes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Campaign
        fields = '__all__'
    
    def get_scenes(self, obj):
        scenes = obj.scene_set.all()
        serializer = SceneSerializer(scenes, many=True)
        return serializer.data


class SceneSerializer(serializers.ModelSerializer):

    nodes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Scene
        fields = '__all__'
    
    def get_nodes(self, obj):
        nodes = obj.scenenode_set.all()
        serializer = SceneNodeSerializer(nodes, many=True)
        return serializer.data


class SceneNodeSerializer(serializers.ModelSerializer):

    choices = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = SceneNode
        fields = '__all__'

    def get_choices(self, obj):
        choices = obj.nodechoice_set.all()
        serializer = NodeChoiceSerializer(choices, many=True)
        return serializer.data

    def get_image(self, obj):
        if obj.background_image:
            return obj.background_image.image.url
        else:
            return ""

class NodeChoiceSerializer(serializers.ModelSerializer):

    icon = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = NodeChoice
        fields = '__all__'
    
    def get_icon(self, obj):
        if obj.icon_linked:
            return obj.icon_linked.image.url
        else:
            return ""