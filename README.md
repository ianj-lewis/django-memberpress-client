# Django Plugin For memberpress REST API Client

[![pypi django-memberpress-client](https://img.shields.io/static/v1?label=pypi&style=flat-square&color=0475b6&message=django-memberpress-client)](https://pypi.org/project/django-memberpress-client/) [![memberpress](https://img.shields.io/static/v1?label=memberpress&style=flat-square&color=04d4e4&message=REST%20API)](https://memberpress.com/addons/developer-tools/) [![hack.d Lawrence McDaniel](https://img.shields.io/badge/hack.d-Lawrence%20McDaniel-orange.svg)](https://lawrencemcdaniel.com)

![memberpress](https://memberpress.com/wp-content/uploads/2022/01/memberpress-logo-color.svg)

A lightweight, performant Django plugin that implements REST api and Webhook integrations for the [Wordpress](https://wordpress.org/) [memberpress](https://memberpress.com/blog/memberpress-developer-tools/) Pro plugin.

## Installation

```bash
pip install django-memberpress-client
```

Set the Django settings using tutor.

```python
from django.conf import settings

settings.MEMBERPRESS_API_KEY = 'set-me-please'
settings.MEMBERPRESS_API_BASE_URL = 'https://set-me-please.com/'
```

You'll find the memberpress API Key in the Wordpress admin site.
![memberpress API Key](doc/memberpress-api-key.png "memberpress API Key")

## Usage

### REST API

```python
from memberpress_client.member import Member

# 1. passing an explicit Wordpress username
member = Member(username="jsmith")
print(member.is_active_subscription)
print(member.is_trial_subscription)
print(member.should_raise_paywall)
print(member.latest_transaction.amount)
print(member.recent_subscriptions[0].created_at)
print(member.active_memberships[0].pricing_title)

# 2. using with Django request object
member = Member(request=request)

# 3. passing a Django user object
member = Member(user=user)

# 4. passing a Django user object
member = Member(user=user)

# 5. passing an json return object from memberpress REST API
member = Member(response=memberpress_response_json)
```

### Webhooks

You can setup this plugin to receive events via memberpress' webhooks framework, a Pro 'developer tools' premium option of memberpress. Add a url of the form https://yourdomain.com/mp/api/v1/webhook to the Developer "Webhooks" page.
![memberpress webhooks](doc/memberpress-api-webhook.png "memberpress webhooks")

urls:

- https://yourdomain.com/mp/api/v1/events/
- https://yourdomain.com/mp/api/v1/events/log/


## Developers

### class hierarchy

```python
class Memberpress:

    class MemberpressEvent(Memberpress):

    class MemberpressAPIClient(Memberpress):
        class Member(MemberpressAPIClient):
        class Membership(MemberpressAPIClient):
        class Subscriber(MemberpressAPIClient):
        class Transaction(MemberpressAPIClient):
```

### constants

- MemberpressEvents: discrete list of memberpress event types. The str value exactly matches the event dict key "event".
- MemberpressEventTypes: discrete list of memberpress event_types
