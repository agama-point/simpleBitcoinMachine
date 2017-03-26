"""Utilities."""
import re
import datetime

def first(iterable, default=None):
    """Get first occurance of an item in itereable."""
    for item in iterable:
        return item
    return default

def parse_utc(timestamp):
    """Parse utc timestamp to datetime."""
    conformed_timestamp = re.sub(r"[:]|([-](?!((\d{2}[:]\d{2})|(\d{4}))$))", '', timestamp)
    return datetime.datetime.strptime(conformed_timestamp, "%Y%m%dT%H%M%S%fZ" )
