from lxml import html
import requests

from listing import Listing
from util.database import Database
from util.gmail import Gmail

config = {
    'max_price': "3000",
    'address': 'M5S+1A1',
    'long_lat': '43.660917,-79.396091',
    'distance': '10.0'
}
u_of_t_address = "40 St George St, Toronto, ON M5S 2E4"
post_name_xpth_prefix = '//*[@id="MainContainer"]/div[4]/div[3]/div/div['
post_name_xpth_suffix = ']/div/div[2]/div/div[2]/a'
last_page = None

base_url = 'http://www.kijiji.ca'

db = Database()
mail = Gmail()

while (True):
    page_number = 1
    for page_number in range(1, 6):
        page_text = 'page-' + str(page_number) + "/" if page_number != 1 else ""

        URL = "http://www.kijiji.ca/b-2-bedroom-apartments-condos/city-of-toronto/" + page_text + \
              "c214l1700273r" + config['distance'] + "?price=__" + config['max_price'] + "&address=" + config[
                  'address'] + "&ll=" + \
              config['long_lat']

        page = requests.get(URL)
        # Break condition to start back at page 1
        if page == last_page:
            break
        else:
            print('PAGE ' + str(page_number) + '============================================')
            last_page = page

        tree = html.fromstring(page.content)

        for i in range(0, 100):
            x_pth = post_name_xpth_prefix + str(i) + post_name_xpth_suffix
            name = tree.xpath(x_pth)

            # If this element does not exist, continue
            if len(name) == 0:
                continue

            lst = Listing(base_url + name[0].attrib['href'])

            print(lst.get_title())
            if lst.get_title() != 'poor_err':
                if not db.listing_exists(lst):
                    db.save_listing(lst, u_of_t_address)
                    if lst.get_viability(u_of_t_address) <= 200 and 'Wanted: ' not in lst.get_title():
                        mail.notify(lst, ["stefan.stancu15@gmail.com", "rhealchan98@gmail.com"], u_of_t_address)
                    print('** New listing saved **')
                else:
                    print('already saved')

            else:
                mail.email_dev(lst.url + "\n broke at \n" + URL, ["stefan.stancu15@gmail.com"])
