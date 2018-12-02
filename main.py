import logging

from hev import config


def main():
    """Cloud Function entrypoint."""
    try:
        api = config.init()
    except RuntimeError as e:
        logging.critical("Unable to configure Cloud Function: %s", str(e))
        return

    # Collect values from Cloud Datastore
    # TODO: NotImplemented
    bpm, value_min, value_max = 70, 80, 144

    # Send values to Datadog
    api.send_bpm(bpm)
    api.send_pressure(value_min, value_max)

    logging.info("Cloud Function executed correctly.")
