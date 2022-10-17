import logging

from rest_framework.views import APIView
from django.http import HttpResponse

from memberpress_client.decorators import app_logger
from memberpress_client.event import get_event
from memberpress_client.models import MemberpressEvents

logger = logging.getLogger(__name__)


class EventView(APIView):
    @app_logger
    def put(self, request):
        user = request.user
        data = request.POST
        method = "put"

        user = user
        data = data
        method = method
        event = get_event(data=data)
        if event.is_valid:
            logger.info(
                "received event: {event} {event_type}. JSON={json}".format(
                    event=event.event, event_type=event.event_type, json=event.json
                )
            )
        MemberpressEvents(sender="fix me", event=event.event, json=event.json).save()
        return HttpResponse(status=201)


class EventLogView(APIView):
    @app_logger
    def get(self, request):
        return HttpResponse("log view")
