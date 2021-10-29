from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import CampaignSerializer, CampaignDataSerializer
from content.models import Campaign
from zcoast.api import serializers


# URL OVERVIEW OF API FUNCTIONS
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        'Campaigns': '/campaigns/',
        'Detail Campaign View': '/campaigns/<str:pk>'
    }
    return Response(api_urls)


# GET LIST OF CAMPAIGNS
@api_view(['GET'])
def campaign_list(request):
    campaigns = Campaign.objects.all()
    serializer = CampaignSerializer(campaigns, many=True)
    return Response(serializer.data)


# GET CAMPAIGN DATA
@api_view(['GET'])
def campaign_data(request, pk):
    campaign = Campaign.objects.get(id=pk)
    serializer = CampaignDataSerializer(campaign, many=False)
    return Response(serializer.data)