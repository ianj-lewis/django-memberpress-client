from django.contrib import admin
from memberpress_client.models import WebHooks


class WebHooksAdmin(admin.ModelAdmin):
    """
    Memberpress Webhook event log
    """

    def has_change_permission(self, request, obj=None):
        return False

    search_fields = ("course_id",)
    list_display = (
        "sender",
        "webhook",
        "json",
        "created",
        "modified",
    )


admin.site.register(WebHooks, WebHooksAdmin)
