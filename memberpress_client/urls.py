"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - url scaffolding
"""
from django.urls import path
from memberpress_client.api import views as api_views

app_name = "memberpress_client"
urlpatterns = [
    path("webhook/", api_views.WebhookView.as_view(), name="webhook"),
]
