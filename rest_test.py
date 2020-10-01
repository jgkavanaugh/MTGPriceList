# TODO: Need to deal with next_page. Need to build aggregate value of rarities and averages

import requests

# Scryfall REST search URL
URL = "https://api.scryfall.com/cards/search?order=cmc&q=e%3Aznr"

# Send a GET request
response = requests.get(url=URL)

# TODO: This needs to raise an exception
if response:
    print('Requests was successful.')
else:
    print('Request returned an error.')

# Save as dict. We will probably need response later again
card_list = response.json()

# Loop to get non-foil prices
for data in card_list['data']:
    if data['nonfoil']:
        print('{} {} {}'.format(data['name'], data['rarity'], data['prices']['usd']))

# Loop to get foil prices
for data in card_list['data']:
    if data['foil']:
        print('{} {} {}'.format(data['name'], data['rarity'], data['prices']['usd_foil']))
