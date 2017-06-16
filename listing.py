"""
    This is the class that holds all the logic for processing a listing and doing all the checks
"""
from lxml import html
import requests
import util.helper as util
import sys
import util.gmaps as gmaps

from util.database import DBListing

cost_xpaths = [
    '//*[@id="itemdetails"]/div[2]/table/tr[2]/td/div/span/strong',
    '//*[@id="itemdetails"]/table/tr[2]/td/div/span/strong'
]

address_xpaths = [
    '//*[@id="itemdetails"]/div[2]/table/tr[3]/td',
    '//*[@id="itemdetails"]/table/tr[3]/td'
]

title_xpath = '//*[@id="MainContainer"]/div[4]/div[3]/span/h1'


class Listing:
    def __init__(self, url):
        self.page = requests.get(url)
        self.tree = html.fromstring(self.page.content)
        self.url = url

        # self.db_url = util.get_db_url('credentials/db_credentials.json')

    def get_cost(self):
        """
            Cost of the listing, and also saves it to the object
        Returns:
            (int) the listing cost
        """
        try:
            self.cost
        except AttributeError:
            try:
                cost = util.get_cost_by_xpaths(self.tree, cost_xpaths)
                self.cost = util.string_to_float(cost[0].text)

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
            self.address
        except AttributeError:
            try:
                address_elem = util.get_address_by_xpaths(self.tree, address_xpaths)
                self.address = address_elem[0].text
            except:
                print('ERROR: Could not get address value from the site')
                sys.exit(0)

        return self.address

    def get_title(self):
        """
            Gets the post title from the HTML if it does not yet exist. Also sets the property on the object.
        Returns:
            String: The name of the post

        """
        try:
            self.title
        except AttributeError:
            try:
                self.title = self.tree.xpath(title_xpath)[0].text
            except IndexError:
                print('This site broke it:')
                print(self.url)
                self.title = 'poor_err'


        return self.title

    def get_commute_time(self, dest_address):
        """
            Uses Google Maps API to compute the travel time using public transit
        Args:
            dest_address: (string) raw destination address
        Returns:
            (float): The time in minutes of the commute

        """

        gmap = gmaps.Gmap()
        location = gmap.directions(self.get_address(), dest_address)
        time_sec = location[0]['legs'][0]['duration']['value']
        return time_sec/60

    def get_viability(self, dest_address):
        """
            Calculates the viability as a score
        Args:
            dest_address: for the get_commute_time method

        Returns:
            (float): viability score

        """

        return self.get_cost() / 100 * self.get_commute_time(dest_address)
