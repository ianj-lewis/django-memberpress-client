import logging

from rest_framework.views import APIView
from django.http import HttpResponse, HttpResponseNotFound

from memberpress_client.decorators import app_logger

logger = logging.getLogger(__name__)


class WebhookView(APIView):
    @app_logger
    def process_webhook(self, method, user, data):
        pass

    @app_logger
    def put(self, request):
        user = request.user
        data = request.POST
        self.process_webhook(method="put", user=user, date=data)
        return HttpResponse(status=201)

    @app_logger
    def patch(self, request):
        user = request.user
        data = request.POST
        self.process_webhook(method="put", user=user, date=data)
        return HttpResponse(status=201)

    @app_logger
    def get(self, request):
        return HttpResponseNotFound

    @app_logger
    def delete(self, request):
        return HttpResponseNotFound


class WebhookLogView(APIView):
    @app_logger
    def get(self, request):
        return HttpResponse("log view")

    @app_logger
    def put(self, request):
        return HttpResponseNotFound

    @app_logger
    def patch(self, request):
        return HttpResponseNotFound

    @app_logger
    def delete(self, request):
        return HttpResponseNotFound
