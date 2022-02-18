import functools
import os

from datadog import statsd, initialize

from .logger import get_logger


def initialize_dogstats(func):
    """
    Decorator function that initalizes a connection to dogstatsd
    Reads environmental variables for DD_ENDPOINT and DD_PORT
        DD_ENDPOINT: is the IP address of the statsd endpoint being sent to
        DD_PORT: The port that the statsd endpoint is listening on
    """
    @functools.wraps(func)
    def init(*args, **kwargs):
        logger = get_logger(__name__)
        try:
            endpoint = os.environ.get('DD_ENDPOINT', '127.0.0.1')
            port = os.environ.get('DD_PORT', '8125')

            options = {'statsd_host': endpoint, 'statsd_port': port}
            initialize(**options)
            func(*args, **kwargs)
        except Exception as e:
            logger.error(e)
            raise e

    return init


@initialize_dogstats
def send_gauge_to_datadog(
    metric_name: str,
    metric: float,
    tags: list,
):
    """
    Wraps datadog statsd.gauge function with an initalized
    statsd connection 
    """
    statsd.gauge(metric_name, metric, tags=tags)


@initialize_dogstats
def send_event_to_datadog(
    title: str,
    text: str,
    alert_type: str,
    aggregation_key: str = None,
    date: int = None,
    tags: list = None,
    hostname: str = None,
):
    """
    Wraps datadog statsd.event function with an initalized
    statsd connection 
    """
    statsd.event(title=title,
                 text=text,
                 alert_type=alert_type,
                 aggregation_key=aggregation_key,
                 date_happened=date,
                 tags=tags,
                 hostname=hostname)
    
