"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - url scaffolding
"""
from django.urls import include, path

# FIX NOTE: only import if we're running locally.
from django.contrib import admin

app_name = "memberpress_client"
urlpatterns = [
    # FIX NOTE: only import if we're running locally.
    path("mp/api/v1/", include("memberpress_client.api.v1.urls")),
    path("admin/", admin.site.urls),
    # production, as a Django plugin running in a namespace
    path("api/v1/", include("memberpress_client.api.v1.urls")),
]
