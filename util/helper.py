"""
    Helper functions are all placed here
"""
import re
import json


def string_to_float(dirty_string):
    """
        Cleans the cost string from the website
    Args:
        dirty_string: (string)

    Returns:
        float:

    """
    non_decimal = re.compile(r'[^\d.]+')
    return float(non_decimal.sub('', dirty_string))


def get_cost_by_xpaths(root_elem, cost_xpaths):
    """
        Tries all the xpaths for the possible page compositions
    Returns:
        HTMLElement: The html cost element
    Raises:
        ValueError: If there is no value available
    """
    for xpath in cost_xpaths:
        cost_elem = root_elem.xpath(xpath)
        if len(cost_elem) != 0:
            return cost_elem

    raise ValueError


def get_address_by_xpaths(root_elem, address_xpaths):
    """
        Tries all the xpaths for the possible page compositions
    Returns:
        HTMLElement: The html address element
    Raises:
        ValueError: If there is no value available
    """
    for xpath in address_xpaths:
        address_elem = root_elem.xpath(xpath)
        if len(address_elem) != 0:
            return address_elem

    raise ValueError


def get_db_url(path):
    """
        Load the url from a json file, contains credentials
    Args:
        path: (string) the path to the json file

    Returns:
        (string): the database url

    """

    return json.load(open(path))['db_url']
