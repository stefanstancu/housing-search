from lxml import html
import requests

config = {
    'max_price': "2200",
    'address': 'M5S+1A1',
    'long_lat': '43.660917,-79.396091'
}
post_name_xpth_prefix = '//*[@id="MainContainer"]/div[4]/div[3]/div/div['
post_name_xpth_suffix = ']/div/div[2]/div/div[2]/a'
page_number = 0
last_page = None

while (True):

    page_text = 'page-' + str(page_number) + "/" if page_number != 0 else ""

    URL = "http://www.kijiji.ca/b-2-bedroom-apartments-condos/city-of-toronto/" + page_text + \
          "c214l1700273r5.0?price=__" + config['max_price'] + "&address=" + config['address'] + "&ll=" + \
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

        # Do checks on the posting and do whatever we need with it if it works
        

        # If this element does not exist, it will return an empty array
        if len(name) == 0:
            continue
        # Print the postname
        print(name[0].text.strip())

    page_number += 1
