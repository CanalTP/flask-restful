from datetime import datetime
from email.utils import formatdate
import re

# https://code.djangoproject.com/browser/django/trunk/django/core/validators.py
# basic auth added by frank
from calendar import timegm

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:[^:@]+?:[^:@]*?@|)'  # basic auth
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+'
    r'(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
    r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def url(value):
    """Validate a URL.

    :param string value: The URL to validate
    :returns: The URL if valid.
    :raises: ValueError
    """
    if not regex.search(value):
        message = u"{0} is not a valid URL".format(value)
        if regex.search('http://' + value):
            message += u". Did you mean: http://{0}".format(value)
        raise ValueError(message)
    return value


def date(value):
    """Parse a valid looking date in the format YYYY-mm-dd"""
    date = datetime.strptime(value, "%Y-%m-%d")
    if date.year < 1900:
        raise ValueError(u"Year must be >= 1900")
    return date


def natural(value):
    """Parse a non-negative integer value"""
    value = int(value)
    if value < 0:
        raise ValueError("Invalid literal for natural(): '{}'".format(value))
    return value


def boolean(value):
    """Parse the string ``"true"`` or ``"false"`` as a boolean (case
    insensitive). Also accepts ``"1"`` and ``"0"`` as ``True``/``False``
    (respectively). If the input is from the request JSON body, the type is
    already a native python boolean, and will be passed through without
    further parsing.
    """
    if isinstance(value, bool):
        return value

    if isinstance(value, int):
        return bool(value)

    if not value:
        raise ValueError("boolean type must be non-null")
    value = value.lower()
    if value in ('true', '1'):
        return True
    if value in ('false', '0'):
        return False
    raise ValueError("Invalid literal for boolean(): {}".format(value))


def rfc822(dt):
    return formatdate(timegm(dt.utctimetuple()))
