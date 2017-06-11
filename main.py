from lxml import html
import requests

config = {
    'max_price': 2200,
    'address': 'M5S+1A1',
    'long_lat': '43.660917,-79.396091'
}

page = requests.get("http://www.kijiji.ca/b-2-bedroom-apartments-condos/city-of-toronto/c214l1700273r5.0?price=__" +
                    config['max_price'] + "&address=" + config['address'] + "&ll=" + config['long_lat'])

tree = html.fromstring(page.content)

post_name_xpth_prefix = '//*[@id="MainContainer"]/div[4]/div[3]/div/div['
post_name_xpth_suffix = ']/div/div[2]/div/div[2]/a'

for i in range(6, 33):
    x_pth = post_name_xpth_prefix + str(i) + post_name_xpth_suffix
    name = tree.xpath(x_pth)

    # If this element does not exist, it will return an empty array
    if len(name) == 0:
        continue
    print(name[0].text)
