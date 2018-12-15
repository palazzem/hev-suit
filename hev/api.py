import logging
import datadog

from .exceptions import BadRequest


class DatadogAPI(object):
    """API abstraction built on top of Datadog API. This instance can
    hides Datadog implementation details, such as "Host", "Tags" and
    metrics names. Using this instance is suggested for the scope of
    the Cloud Function.

    Initializing this class has a side-effect that is initializing
    the static Datadog API class.
    """

    def __init__(self, api_key, function_name, dry_run=False):
        # Init Datadog API
        options = {"api_key": api_key}
        datadog.initialize(**options)
        self._api = datadog.api
        self._function_name = function_name
        self._dry_run = dry_run

    def send_bpm(self, value):
        """Sends heart BPM to Datadog."""
        if self._dry_run:
            # dry-run a success
            return True

        response = self._api.Metric.send(
            host=self._function_name, metric="hev.parameters.bpm", points=value
        )

        if response.get("status") != "ok":
            logging.error(response)
            return False
        else:
            return True

    def send_pressure(self, value, kind=None):
        """Sends pressure metrics to Datadog."""
        if self._dry_run:
            # dry-run a success
            return True

        tags = [kind] if kind is not None else None

        response = self._api.Metric.send(
            host=self._function_name,
            metric="hev.parameters.pressure",
            points=value,
            tags=tags,
        )

        if response.get("status") != "ok":
            logging.error(response)
            return False
        else:
            return True


class DialogFlowRequest(object):
    """DialogFlow request class used to validate received data.
    Any interaction with the DialogFlow service must be
    encapsulated in this class.
    """

    MANDATORY = ["bpm", "min", "max"]

    def __init__(self, request):
        """Wrap Flask Request instance that contains DialogFlow data.
        The constructor stores parsed JSON data.

        Args:
            request: Flask Request instance.

        Returns:
            A DialogFlow request instance that contains utility methods
            to manipulate and retrieve parameters.
        """
        self._data = request.get_json(silent=True)

    def validate(self):
        """Validate DialogFlowRequest to be sure it contains expected data.

        Returns:
            A boolean (True) if the request passes this validator.

        Raises:
            BadRequest: malformed data must abort the function execution
        """
        if self._data is None:
            raise BadRequest("Malformed request")

        missing = []
        for field in self.MANDATORY:
            if self.get_parameter(field) is None:
                missing.append(field)

        if missing:
            raise BadRequest("Missing mandatory fields: {}".format(missing))

        return True

    def get_parameter(self, param):
        """Get the DialogFlow parameter.

        Args:
            param: the parameter name to extract

        Returns:
            The DialogFlow parameter, or `None` if not present
        """
        try:
            result = self._data["queryResult"]["parameters"][param]
        except KeyError:
            result = None

        return result
