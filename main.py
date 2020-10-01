# Use three letter codes to pull in set values

import requests
import time
import sys

set_code = input("Three-letter set code: ")
print(set_code)

# Scryfall REST search URL
URL = "https://api.scryfall.com/cards/search?order=cmc&q=e%3A{}".format(set_code)

# Send a GET request
print("Sending request...")
time.sleep(.1)
response = requests.get(url=URL)

# TODO: This needs to raise an exception
if response:
    print('Requests was successful.')
else:
    print('Request returned an error.')

# Save as dict. We will probably need response later again
card_list = response.json()

# Price and counts
cards = {'foil': {'common': {'card_count': 0, 'card_value': 0.0},
                  'uncommon': {'card_count': 0, 'card_value': 0.0},
                  'rare': {'card_count': 0, 'card_value': 0.0},
                  'mythic': {'card_count': 0, 'card_value': 0.0}},
         'nonfoil': {'common': {'card_count': 0, 'card_value': 0.0},
                     'uncommon': {'card_count': 0, 'card_value': 0.0},
                     'rare': {'card_count': 0, 'card_value': 0.0},
                     'mythic': {'card_count': 0, 'card_value': 0.0}}
         }
page_number = 0
pull_complete = False

# While loop for extra pages
while not pull_complete:
    page_number = page_number + 1
    print("Processing page {}".format(page_number))
    # Loop to get non-foil prices
    try:
        for data in card_list['data']:
            if data['nonfoil']:
                cards['nonfoil'][data['rarity']]['card_value'] = cards['nonfoil'][data['rarity']]['card_value'] \
                                                                 + float(data['prices']['usd'])
                cards['nonfoil'][data['rarity']]['card_count'] = cards['nonfoil'][data['rarity']]['card_count'] + 1
    except KeyError:
        print("It appears this key does not exist")
        sys.exit(1)
    # Loop to get foil prices
    for data in card_list['data']:
        if data['foil'] and data['prices']['usd_foil'] is not None:
            cards['foil'][data['rarity']]['card_value'] = cards['foil'][data['rarity']]['card_value'] \
                                                             + float(data['prices']['usd_foil'])
            cards['foil'][data['rarity']]['card_count'] = cards['foil'][data['rarity']]['card_count'] + 1
    if card_list['has_more']:
        time.sleep(.1)
        response = requests.get(card_list['next_page'])
        card_list = response.json()
    else:
        pull_complete = True

print('Foil Values')
for k, v in cards['foil'].items():
    try:
        avg_value = v['card_value']/v['card_count']
    except ZeroDivisionError:
        avg_value = 0
    print('{}: {} {} {}'.format(k, v['card_count'], round(v['card_value'], 2), round(avg_value, 2)))

print('Nonfoil Values')
for k, v in cards['nonfoil'].items():
    try:
        avg_value = v['card_value']/v['card_count']
    except ZeroDivisionError:
        avg_value = 0
    print('{}: {} {} {}'.format(k, v['card_count'], round(v['card_value'], 2), round(avg_value, 2)))