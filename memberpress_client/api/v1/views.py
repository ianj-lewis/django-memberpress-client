import logging

from rest_framework.views import APIView
from django.http import HttpResponse

from memberpress_client.decorators import app_logger

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
        return HttpResponse(status=201)


class EventLogView(APIView):
    @app_logger
    def get(self, request):
        return HttpResponse("log view")
