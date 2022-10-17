# Generated by Django 3.2.13 on 2022-10-17 00:18

from django.db import migrations, models
import django.utils.timezone
import jsonfield.fields
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="MemberpressEvents",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, editable=False, verbose_name="modified"
                    ),
                ),
                (
                    "sender",
                    models.URLField(
                        blank=True, help_text="The site referrer. Example: https://wordpress-site.com/mb/webhooks/"
                    ),
                ),
                (
                    "event",
                    models.CharField(
                        choices=[
                            ("after_cc_expires_reminder", "after_cc_expires_reminder"),
                            ("after_member_signup_reminder", "after_member_signup_reminder"),
                            ("after_signup_abandoned_reminder", "after_signup_abandoned_reminder"),
                            ("after_sub_expires_reminder", "after_sub_expires_reminder"),
                            ("before_cc_expires_reminder", "before_cc_expires_reminder"),
                            ("before_sub_expires_reminder", "before_sub_expires_reminder"),
                            ("before_sub_renews_reminder", "before_sub_renews_reminder"),
                            ("before_sub_trial_ends", "before_sub_trial_ends"),
                            ("login", "login"),
                            ("member_account_updated", "member_account_updated"),
                            ("member_added", "member_added"),
                            ("member_deleted", "member_deleted"),
                            ("member_signup_completed", "member_signup_completed"),
                            ("mpca_course_completed", "mpca_course_completed"),
                            ("mpca_course_started", "mpca_course_started"),
                            ("mpca_lesson_completed", "mpca_lesson_completed"),
                            ("mpca_lesson_started", "mpca_lesson_started"),
                            ("mpca_quiz_attempt_completed", "mpca_quiz_attempt_completed"),
                            ("non_recurring_transaction_completed", "non_recurring_transaction_completed"),
                            ("non_recurring_transaction_expired", "non_recurring_transaction_expired"),
                            ("offline_payment_complete", "offline_payment_complete"),
                            ("offline_payment_pending", "offline_payment_pending"),
                            ("offline_payment_refunded", "offline_payment_refunded"),
                            ("recurring_transaction_completed", "recurring_transaction_completed"),
                            ("recurring_transaction_expired", "recurring_transaction_expired"),
                            ("recurring_transaction_failed", "recurring_transaction_failed"),
                            ("renewal_transaction_completed", "renewal_transaction_completed"),
                            ("sub_account_added", "sub_account_added"),
                            ("sub_account_removed", "sub_account_removed"),
                            ("subscription_created", "subscription_created"),
                            ("subscription_downgraded_to_one_time", "subscription_downgraded_to_one_time"),
                            ("subscription_downgraded_to_recurring", "subscription_downgraded_to_recurring"),
                            ("subscription_downgraded", "subscription_downgraded"),
                            ("subscription_expired", "subscription_expired"),
                            ("subscription_paused", "subscription_paused"),
                            ("subscription_resumed", "subscription_resumed"),
                            ("subscription_stopped", "subscription_stopped"),
                            ("subscription_upgraded_to_one_time", "subscription_upgraded_to_one_time"),
                            ("subscription_upgraded_to_recurring", "subscription_upgraded_to_recurring"),
                            ("subscription_upgraded", "subscription_upgraded"),
                            ("transaction_completed", "transaction_completed"),
                            ("transaction_expired", "transaction_expired"),
                            ("transaction_failed", "transaction_failed"),
                            ("transaction_refunded", "transaction_refunded"),
                            ("unidentified_event", "unidentified_event"),
                        ],
                        help_text="The kind of memberpress event. Examples: ",
                        max_length=50,
                    ),
                ),
                (
                    "json",
                    jsonfield.fields.JSONField(
                        blank=True, default=dict, help_text="A json dict sent by the webhook event in the request body."
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "memberpress events",
            },
        ),
    ]
