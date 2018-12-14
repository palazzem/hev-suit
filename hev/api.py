import logging
import datadog


class DatadogAPI(object):
    """API abstraction built on top of Datadog API. This instance can
    hides Datadog implementation details, such as "Host", "Tags" and
    metrics names. Using this instance is suggested for the scope of
    the Cloud Function.

    Initializing this class has a side-effect that is initializing
    the static Datadog API class.
    """
    def __init__(self, api_key, function_name):
        # Init Datadog API
        options = {
            "api_key": api_key,
        }
        datadog.initialize(**options)
        self._api = datadog.api
        self._function_name = function_name

    def send_bpm(self, value):
        """Sends heart BPM to Datadog."""
        response = self._api.Metric.send(
            host=self._function_name,
            metric="hev.parameters.bpm",
            points=value,
        )

        if response.get("status") != "ok":
            logging.error(response)

    def send_pressure(self, value, kind=None):
        """Sends pressure metrics to Datadog."""
        tags = [kind] if kind is not None else None

        response = self._api.Metric.send(
            host=self._function_name,
            metric="hev.parameters.pressure",
            points=value,
            tags=tags,
        )

        if response.get("status") != "ok":
            logging.error(response)
