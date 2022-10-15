from django.urls import path
from memberpress_client.api.v1 import views

app_name = "memberpress_client"
urlpatterns = [
    path("webhook/", views.WebhookView.as_view(), name="webhook"),
]
