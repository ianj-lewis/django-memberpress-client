# CHANGE LOG

## Version 0.0.7 (2022-10-19)

- bug fixes. remove django-environ and validators from INSTALLED_APPS

## Version 0.0.6 (2022-10-17)

- validate event.setter against MemberpressEvents.all_events()
- validate event_type.setter against MemberpressEventTypes.all_event_types()
- add more event tests
- createe .env-sample for local and production

## Version 0.0.5 (2022-10-17)

- Add webhook event classes, listener and model
- Create base class Membership() and refactor
- Build unit tests for api and webhook events
- Create a Makefile

## Version 0.0.4 (2022-10-14)

- Operational but experimental plugin. Do not use in production.
- Implements REST API only.
- All redundant code moved to the base class
- Added should_raise_paywall property

## Version 0.0.2 (2022-10-13)

- Experimental plugin. Do not use in production.
