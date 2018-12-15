# HEV (Hazardous Environment Suit)

HEV suit is a Python project that runs on [Google Cloud Functions][2]. It accepts requests from any
kind of REST client, even though the format is specific for [DialogFlow requests][1].
The design is the following:

* Google Assistant is used as a main input system
* Using a DialogFlow Agent, natural language processing happens to extract some values
  from the user `Intent`
* DialogFlow Agent communicates with the Cloud Function through a REST API using a Bearer
  Token for the authorization step
* The Cloud Functions parse and process the DialogFlow request and sends some metrics
  back to Datadog
* Datadog dashboards are used to see reported metrics, using monitors for real-time
  alerting

[1]: https://dialogflow.com/docs/fulfillment/how-it-works#request_format
[2]: https://cloud.google.com/functions/

## Requirements

* Python 3.7
* Google Cloud Functions
* Datadog API

## Getting Started

As a first step the application must be [deployed][3] as a Cloud Function. More instructions
will be available as soon the project is used on a personal environment.

[3]: https://cloud.google.com/functions/docs/deploying/filesystem

## Planned Improvements

The project is fairly new and it's mostly a toy project to explore [Actions on Google][4]
and the interaction with Cloud Functions. Having Datadog as a hard dependency has been 
decided to keep the first version simple and easy to manage.

Said that, follows a list of planned improvements:

* Make `DialogFlow` class generic enough to be an external package re-usable
  in other projects
* Make `DatadogAPI` an exporter class that honors a generic interface of
  a plugin system. That way, the Cloud Function acts as a dispatcher to "1 : many"
  services, where Datadog is just the first implementation
* The base framework is Flask because it's used inside Google
  Cloud Functions. As improvement, the web framework may be abstracted, so when a cloud function
  is implemented, a Flask endpoint is generated automatically. This reduces heavily
  the boilerplate to populate Flask `app`. On top of it, having a `py.test` fixture improves
  a lot webhooks testing.

[4]: https://developers.google.com/actions/

## Development

We accept external contributions even though the project is mostly designed for personal
needs. If you think some parts can be exposed with a more generic interface, feel free to
open a GitHub issue and to discuss your suggestion.

### Coding Guidelines

We use [flake8][5] as a style guide enforcement. Said that, we also use [black][6] to
reformat our code, keeping a well defined style even for quotes, multi-lines blocks and other.
Before submitting your code, be sure to launch `black` to reformat your PR.

[5]: https://pypi.org/project/flake8/
[6]: https://github.com/ambv/black

### Testing

`tox` is used to execute the following test matrix:
* `lint`: launches `flake8` and `black --check` to be sure the code honors our style guideline
* `py37`: launches `py.test` to execute all tests under Python 3.7

To launch the test matrix, just:

```bash
$ tox
```
