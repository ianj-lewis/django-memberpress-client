"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - url scaffolding
"""
from django.urls import include, path

app_name = "memberpress_client"
urlpatterns = [
    path("api/v1/", include("memberpress_client.api.v1.urls")),
]
