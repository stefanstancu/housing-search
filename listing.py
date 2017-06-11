"""
    This is the class that holds all the logic for processing a listing and doing all the checks
"""
from lxml import html
import requests
import util.helper as util
import sys

cost_xpaths = ['//*[@id="itemdetails"]/div[2]/table/tr[2]/td/div/span/strong',
               '//*[@id="itemdetails"]/table/tr[2]/td/div/span/strong']


class Listing:
    def __init__(self, url):
        # Get the listing
        self.url = url
        self.page = requests.get(url)
        self.tree = html.fromstring(self.page.content)
        self.cost = 0.0

    def get_cost(self):
        """
            Returns the cost of the listing, and also saves it to the object
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
