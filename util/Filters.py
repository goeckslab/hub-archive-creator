import logging

class TraceBackFormatter(logging.Formatter):
    def format(self, record):
        # If the log has some Exception text, we don't display them
        s = super(TraceBackFormatter, self).format(record)
        if record.exc_text or record.exc_info:
            s = record.message
        return s
