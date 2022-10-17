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


class MemberpressEvents(TimeStampedModel):
    """ """

    class Meta:
        verbose_name_plural = "memberpress events"

    sender = models.URLField(
        blank=True,
        help_text=_("The site referrer. Example: https://wordpress-site.com/mb/webhooks/"),
    )

    event = models.CharField(
        blank=False,
        choices=MEMBERPRESS_EVENTS,
        max_length=50,
        help_text=_("The kind of memberpress event. Examples: "),
    )

    json = jsonfield.JSONField(
        blank=True,
        help_text=_("A json dict sent by the webhook in the request body."),
    )

    def __str__(self):
        return str(self.created) + "-" + self.webhook
