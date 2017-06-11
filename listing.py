"""
    This is the class that holds all the logic for processing a listing and doing all the checks
"""
from lxml import html
import requests
import util.helper as util
import sys

cost_xpaths = [
    '//*[@id="itemdetails"]/div[2]/table/tr[2]/td/div/span/strong',
    '//*[@id="itemdetails"]/table/tr[2]/td/div/span/strong'
]

address_xpaths = [
    '//*[@id="itemdetails"]/div[2]/table/tr[3]/td',
    '//*[@id="itemdetails"]/table/tr[3]/td'
]

class Listing:
    def __init__(self, url):
        # Get the listing
        self.url = url
        self.page = requests.get(url)
        self.tree = html.fromstring(self.page.content)
        self.cost = 0.0
        self.address = "Default"

    def get_cost(self):
        """
            Cost of the listing, and also saves it to the object
        Returns:
            (int) the listing cost
        """
        try:
            cost = util.get_cost_by_xpaths(self.tree, cost_xpaths)
            self.cost = util.clean_cost(cost[0].text)

        except ValueError:
            print('ERROR: Could not get cost value from the site')
            sys.exit(0)

        return self.cost

    def get_address(self):
        """
            Gets the address from the HTML. Saves it to the object and also geocodes it
        Returns:
            String: The raw address from the HTML

        """
        try:
            address_elem = util.get_address_by_xpaths(self.tree, address_xpaths)
            self.address = address_elem[0].text
        except:
            print('ERROR: Could not get address value from the site')
            sys.exit(0)

        return self.address

    def get_commute_time(self):
        """
            Uses Google Maps API to compute the travel time using public transit
        Returns:
            Int: The time in minutes of the commute

        """

        # If there is no address on the object, run get_address
        if self.address == "Default":
            self.get_address()
