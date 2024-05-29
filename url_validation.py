# -*- coding: utf-8 -*-
"""
Created on Fri May 24 18:19:20 2024

@author: SWannell
"""

from urllib.parse import urlparse, parse_qs
import json
import re

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


#%% Actually do checks

with open('checks\\generated_urls.json') as f:
    output_to_check = json.load(f)

review_state = True
for k in output_to_check.keys():
    for v in output_to_check[k]:
        if not basic_checks(v):
            review_state = False
            print(f'In checking {k} links, {v} failed')

if review_state:
    print("All passed!")

# At this point, check them in the checker
# One day, migrate these checks into a Python checker