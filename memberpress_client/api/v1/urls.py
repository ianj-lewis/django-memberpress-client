from django.urls import path
from memberpress_client.api.v1 import views

app_name = "memberpress_client_api"
urlpatterns = [
    path("events/", views.EventView.as_view(), name="events"),
    path("events/log/", views.EventLogView.as_view(), name="events_log"),
]
