"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - url scaffolding
"""
from django.urls import include, path

app_name = "memberpress_client"
urlpatterns = [
    # local development running as a Django project
    path("mp/api/v1/", include("memberpress_client.api.v1.urls")),
    # production, as a Django plugin running in a namespace
    path("api/v1/", include("memberpress_client.api.v1.urls")),
]
