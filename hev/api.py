import logging
import datadog


class API(object):
    """API abstraction built on top of Datadog API. This instance can
    hides Datadog implementation details, such as "Host", "Tags" and
    metrics names. Using this instance is suggested for the scope of
    the Cloud Function.
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
            metric="body.parameters.bpm",
            points=value,
        )

        if response.get("status") != "ok":
            logging.error(response)

    def send_pressure(self, value_min, value_max):
        """Sends pressure metrics to Datadog."""
        # Min pressure
        response = self._api.Metric.send(
            host=self._function_name,
            metric="body.parameters.pressure",
            points=value_min,
            tags=["min"],
        )

        if response.get("status") != "ok":
            logging.error(response)

        # Max pressure
        response = self._api.Metric.send(
            host=self._function_name,
            metric="body.parameters.pressure",
            points=value_max,
            tags=["max"],
        )

        if response.get("status") != "ok":
            logging.error(response)
