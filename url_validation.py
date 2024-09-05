# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:19:20 2024

@author: SWannell
"""

from urllib.parse import urlparse, parse_qs
import json
import re
import copy  # as 'shallow copy' of dicts updates the source dict too

trial_url = 'https://donate.redcross.org.uk/appeal/general-fund-appeal?&utm_campaign=General%20Fund%20Appeal&utm_source=Spotify&utm_medium=Audio&utm_content=Donate%20Landing_CTA&utm_term=246802_Interest_Non-science%20nerds&utm_id=123456&c_id=123456&utm_marketing_tactic=Donation&c_name=General%20Fund%20Appeal&c_source=Spotify&c_medium=Audio&c_creative=Donate%20Landing_CTA&c_code=246802&adg=Interest_Non-science%20nerds&#appeal-intro'
parsed_url = urlparse(trial_url)
parsed_qs = parse_qs(parsed_url.query)

params = ['utm_campaign', 'utm_source', 'utm_medium', 'utm_content',
          'utm_term', 'utm_id', 'c_id',  'utm_marketing_tactic', 'c_name',
          'c_source', 'c_medium', 'c_creative', 'c_code', 'adg']

def basic_checks(url):
    parsed_url = urlparse(url)
    check_state = True
    if '&&' in url:
        check_state = False
        print("Double ampersand")
    elif parsed_url.scheme != 'https':
        check_state = False
        print("Not https")
    elif ' ' in url:
        check_state = False
        print("Space in the URL")
    for p in params:
        if p in url:
            if re.search(f'.*[^\?&]{p}=.*', url):
                check_state = False
                print("Badly-formed parameter")
    return check_state

assert basic_checks("https://www.redcross.org.uk?utm_campaign=123&utm_term=456")
assert basic_checks("https://www.redcross.org.uk?utm_campaign=123&&utm_term=456") == False
assert basic_checks("http://www.redcross.org.uk?utm_campaign=123&utm_term=456") == False
assert basic_checks("https://www.redcross.org.uk?utm_campaign=123&utm_term=4 56") == False
assert basic_checks("https://www.redcross.org.uk?utm_campaign=123utm_term=456") == False


#%% Import data

with open('checks\\generated_urls.json') as f:
    output_to_check = json.load(f)
    
#%% Check URLs: hygiene checks

review_state = True
for k in output_to_check.keys():
    for v in output_to_check[k]:
        if not basic_checks(v):
            review_state = False
            print(f'In checking {k} links, {v} failed')

if review_state:
    print("All passed!")

# At this point, check them in the checker
# One day, migrate these checks into a Python checker -- some bits done below

#%% Get and set up data to check URLs

compare_parameters = {
    'utm_campaign': 'c_name',
    'utm_source': 'c_source',
    'utm_medium': 'c_medium',
    'utm_content': 'c_creative',
    'utm_id': 'c_id',
    }

# output_with_mistake = copy.deepcopy(output_to_check)
# output_with_mistake['offline'][0] = 'https://donate.redcross.org.uk/appeal/myanmar-appeal?utm_campaign=Myanmar%20Appeal&utm_source=Door%20Drop&utm_medium=Offline&utm_content=Donate%20Landing_2019%2001_URL%20winte&utm_term=175154_Cold%20Supporters&c_name=Myanmar%20Appeal&c_source=Door%20Drop&c_medium=Offline&c_creative=Donate%20Landing_2019%2001_URL%20winter&c_code=175154&adg=Col%20Supporters'
# data_to_check = copy.deepcopy(output_with_mistake)
data_to_check = copy.deepcopy(output_to_check)

#%% Check URLs: parameter equivalence

for k in data_to_check.keys():
    review_state = True
    for v in data_to_check[k]:
        parsed_url = urlparse(v)
        parsed_qs = parse_qs(parsed_url.query)
        # Check all basic match parameters
        for utm_q, c_q in compare_parameters.items():
            # If both sets of queries are on the link
            if (utm_q in parsed_qs.keys()) and (c_q in parsed_qs.keys()):
                if parsed_qs[utm_q] != parsed_qs[c_q]:
                    print(f'! In checking {k} links, there was an issue ' \

                              f'where {utm_q} != {c_q}')
                    review_state = False
        # Check the audience parameters
        if ('utm_term' in parsed_qs.keys()) and ('adg' in parsed_qs.keys()):
            if parsed_qs['utm_term'] != [parsed_qs['c_code'][0] + '_' + parsed_qs['adg'][0]]:
                print(f"! In checking {k} links, there was an issue " \
                      "where the audience parameters didn't match")
                review_state = False
    if review_state:
        print(f"== ✓ All fine for {k} ==")
    else:
        print(f"== !! Issues found for {k} ==")

#%% Check URLs: correctness checks

# Check 
for v in data_to_check['video']:
    parsed_url = urlparse(v)
    parsed_qs = parse_qs(parsed_url.query)
    assert parsed_qs['spm'] == ['Regular Giving']
print("== ✓ Custom query parameters maintained ==")

for i, v in enumerate(data_to_check['audio']):
    if i!=2:
        parsed_url = urlparse(v)
        parsed_qs = parse_qs(parsed_url.query)
        assert parsed_qs['spm'] == ['Regular Giving']
    if i>=2:
        extr = re.match('.*(\#.*)', v)
        assert extr.group(1) == '#appeal-intro'
print("== ✓ Fragment and/or custom query combo ==")

#%% Check URLs: value correctness

# TBC -- would need to compare to CSV of current check spreadsheet
