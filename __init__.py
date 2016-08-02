# Set default logging handler to avoid "No handler found" warnings.
import logging
import sys

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

logging.getLogger(__name__).addHandler(NullHandler())

log_stdout = None
log_stderr = None


# TODO: Handle the Exception by dispatching the error depending on the (debug) mode
#class Exception(Exception):