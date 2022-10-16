"""
Lawrence McDaniel - https://lawrencemcdaniel.com
Oct-2022

memberpress REST API Client plugin for Django - Models.
"""
from email.policy import default
from django.utils.translation import ugettext as _
from django.db import models
from model_utils.models import TimeStampedModel

# To do: remove this when Open edX moves to Django 3.x
import jsonfield

from memberpress_client.constants import MEMBERPRESS_EVENTS


class WebHooks(TimeStampedModel):
    """ """

    class Meta:
        pass

    sender = models.URLField(
        blank=True,
        help_text=_("The site referrer. Example: https://wordpress-site.com/mb/webhooks/"),
    )

    webhook = models.CharField(
        blank=False,
        choices=MEMBERPRESS_EVENTS,
        max_length=50,
        help_text=_("The kind of webhook. Examples: "),
    )

    json = jsonfield.JSONField(
        blank=True,
        help_text=_("A json dict sent by the webhook in the request body."),
    )

    def __str__(self):
        return str(self.created) + "-" + self.webhook
