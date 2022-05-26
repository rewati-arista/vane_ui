import sys
import collections


def make_iterable(value):
    """Converts the supplied value to a list object
    This function will inspect the supplied value and return an
    iterable in the form of a list.
    Args:
        value (object): An valid Python object
    Returns:
        An iterable object of type list
    """
    if sys.version_info <= (3, 0):
        # Convert unicode values to strings for Python 2
        if isinstance(value, unicode):
            value = str(value)
    if isinstance(value, str) or isinstance(value, dict):
        value = [value]

    if sys.version_info <= (3, 3):
        if not isinstance(value, collections.Iterable):
            raise TypeError('value must be an iterable object')
    else:
        if not isinstance(value, collections.abc.Iterable):
            raise TypeError('value must be an iterable object')

    return value

