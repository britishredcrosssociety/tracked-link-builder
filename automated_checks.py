# -*- coding: utf-8 -*-
"""
Created on Fri May 24 12:31:13 2024

@author: SWannell
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import json

# Use webdriver_manager to avoid version errors when Chrome updates
cService = webdriver.ChromeService(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service = cService)

driver.get(r'C:\\Users\\SWannell\\OneDrive%20-%20British%20Red%20Cross%20Society\\Documents\\Coding\\tracked-link-builder\\index.html');

outputs = {}

def find_element_medium(med, param):
    return driver.find_element(By.CSS_SELECTOR, f"#{med}{param}")

def weird_dropdown(vals, which):
    if which=='campaign':
        driver.find_element(By.CSS_SELECTOR, "p#campaignselect").click()
        time.sleep(1)  # let the JS appear
        driver.find_element(By.CSS_SELECTOR, f"div.dropdown-main ul li[data-value='{vals}']").click()
        time.sleep(1)
    elif which=='socialad':
        for k, v in vals.items():
            driver.find_element(By.CSS_SELECTOR, f"div#socialadaudiencecontainer{k} div.dropdown-chose-list").click()
            time.sleep(1)  # let the JS 
            for el in v:
                driver.find_element(By.CSS_SELECTOR, f"div#socialadaudiencecontainer{k} div.dropdown-main ul li[data-value='{el}']").click()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, 'h2').click()

def clear_multiselect(vals):
    for k, v in vals.items():
        for el in v:
            driver.find_element(By.CSS_SELECTOR, f"i[data-id='{el}']").click()

#%% Banner

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Banner')
time.sleep(1)
weird_dropdown('Disaster Fund', which='campaign')

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")
taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

domain.send_keys('donate.redcross.org.uk/appeal/disaster-fund')
Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('banner', 'source')).select_by_value('FORO')
find_element_medium('banner', 'adcreative').send_keys('Japan Earthquake')
find_element_medium('banner', 'audience1').send_keys('Home Page')
find_element_medium('banner', 'audience2').send_keys('Search Page')
urls = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['banner'] = url_list

Select(find_element_medium('banner', 'source')).select_by_value('MediaMath')
Select(find_element_medium('banner', 'ownsourcecode')).select_by_value('Yes')
time.sleep(1)
find_element_medium('banner', 'sourcecode1').send_keys('123')
find_element_medium('banner', 'sourcecode2').send_keys('456')
urls = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['banner'] += url_list

#%% Paid Video

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Paid Video')
time.sleep(1)
weird_dropdown('General Fund Appeal', which='campaign')

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")
taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

domain.send_keys('donate.redcross.org.uk/appeal/general-fund-appeal?spm=Regular%20Giving')
Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('video', 'source')).select_by_value('Channel4')
Select(find_element_medium('video', 'adtype')).select_by_value('Interest')
find_element_medium('video', 'adcreative').send_keys('CTA')
find_element_medium('video', 'audience1').send_keys('Science nerds')
url = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
outputs['video'] = [url]

Select(find_element_medium('video', 'ownsourcecode')).select_by_value('Yes')
time.sleep(1)
find_element_medium('video', 'sourcecode1').send_keys('135791')
url = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
outputs['video'].append(url)

#%% Audio

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Audio')
time.sleep(1)
weird_dropdown('General Fund Appeal', which='campaign')

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")
taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

domain.send_keys('donate.redcross.org.uk/appeal/general-fund-appeal?spm=Regular%20Giving')
Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('audio', 'source')).select_by_value('Spotify')
Select(find_element_medium('audio', 'adtype')).select_by_value('Interest')
find_element_medium('audio', 'adcreative').send_keys('CTA')
find_element_medium('audio', 'audience1').send_keys('Science nerds')
url = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
outputs['audio'] = [url]

find_element_medium('audio', 'ownsourcecode').send_keys('Yes')
time.sleep(1)
find_element_medium('audio', 'sourcecode1').send_keys('246802')
url = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
outputs['audio'].append(url)

domain.clear()
domain.send_keys("https://donate.redcross.org.uk/appeal/general-fund-appeal#appeal-intro")
url = driver.find_element(By.CSS_SELECTOR, "textarea#url").get_attribute('value')
outputs['audio'].append(url)

domain.clear()
domain.send_keys("https://donate.redcross.org.uk/appeal/general-fund-appeal?spm=Regular%20Giving#appeal-intro")
find_element_medium('audio', 'audience2').send_keys('Non-science nerds')
find_element_medium('audio', 'sourcecode2').send_keys('246802')
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['audio'].append(url_list[-1])

#%% Paid social

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Paid Social')
time.sleep(1)

taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")
domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")

vals_fb = {1: ['Women', '25-34'], 2: ['Men', '55 Plus'], 3: ['65 Plus', 'Walking and Hiking']}

weird_dropdown('General Fund Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/general-fund-appeal')
Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('socialad', 'source')).select_by_value('Facebook')
time.sleep(1)
find_element_medium('socialad', 'adtype_facebook').send_keys('Video')
find_element_medium('socialad', 'adcreative').send_keys('Aleppo Attack')
weird_dropdown(vals_fb, which='socialad')
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['socialad'] = url_list

Select(find_element_medium('socialad', 'source')).select_by_value('Instagram')
find_element_medium('socialad', 'adtype_facebook').send_keys('Image')
find_element_medium('socialad', 'ownsourcecode').send_keys('Yes')
time.sleep(1)
find_element_medium('socialad', 'sourcecode1').send_keys('111')
find_element_medium('socialad', 'sourcecode2').send_keys('222')
clear_multiselect(vals_fb)
vals_ig = {1: ['BRC Page Likers'], 2: ['BRC Page Likers_Friends']}
weird_dropdown(vals_ig, which='socialad')
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['socialad'] += url_list

Select(find_element_medium('socialad', 'source')).select_by_value('LinkedIn')
find_element_medium('socialad', 'adtype_linkedin').send_keys('Sponsored Content_Image')
find_element_medium('socialad', 'ownsourcecode').send_keys('No')
time.sleep(1)
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['socialad'] += url_list

Select(find_element_medium('socialad', 'source')).select_by_value('Twitter')
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['socialad'] += url_list

Select(find_element_medium('socialad', 'source')).select_by_value('TikTok')
find_element_medium('socialad', 'adtype_tiktok').send_keys('In Feed')
find_element_medium('socialad', 'ownsourcecode').send_keys('Yes')
time.sleep(1)
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['socialad'] += url_list

#%% Organic social

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Organic Social')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('UK Fund Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/uk-fund-appeal')
find_element_medium('socialpost', 'source').send_keys('LinkedIn')
time.sleep(1)
find_element_medium('socialpost', 'brc').send_keys('Not BRC')
time.sleep(1)
find_element_medium('socialpost', 'audience').send_keys('Land Rover')
find_element_medium('socialpost', 'linkdetails').send_keys('CTA')
url = final_url.get_attribute('value')
outputs['socialpost'] = [url]

#%% Social share

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Social Share')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Iraq Crisis Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/iraq-crisis-appeal')
find_element_medium('socialshare', 'source').send_keys('Twitter')
time.sleep(1)
find_element_medium('socialshare', 'audience').send_keys('About Us')
find_element_medium('socialshare', 'linkdetails').send_keys('ATC')
url = final_url.get_attribute('value')
outputs['socialshare'] = [url]

#%% Social button

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Social Button')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Lake Chad Crisis Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/lake-chad-crisis-appeal')
find_element_medium('socialbutton', 'source').send_keys('Facebook')
time.sleep(1)
url = final_url.get_attribute('value')
outputs['socialbutton'] = [url]

#%% Email

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Email')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Syria Crisis Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/syria-crisis-appeal')
Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('email', 'source')).select_by_value('Salesforce')
time.sleep(1)
Select(find_element_medium('email', 'sendname')).select_by_value('Fundraising_Donate')
find_element_medium('email', 'sendnumber').send_keys('2')
find_element_medium('email', 'adcreative').send_keys('Aleppo')
Select(find_element_medium('email', 'linklocation1')).select_by_value('Header Button')
Select(find_element_medium('email', 'linklocation2')).select_by_value('Copy Button')
Select(find_element_medium('email', 'linklocation3')).select_by_value('Copy 1')
find_element_medium('email', 'linkcontent1').send_keys('Donate')
find_element_medium('email', 'linkcontent2').send_keys('Give')
find_element_medium('email', 'linkcontent3').send_keys('Help')
urls = final_url.get_attribute('value')
url_list = [i for i in urls.split('\n') if i!='']
outputs['email'] = url_list

domain.clear()
domain.send_keys('https://firstaidchampions.redcross.org.uk/primary/')
weird_dropdown('Community Education_First Aid Champions', which='campaign')
Select(driver.find_element(By.CSS_SELECTOR, "#isIndividual")).select_by_value('No')
Select(marketing_obj).select_by_value('Volunteering')
taxonomy_code.clear()
taxonomy_code.send_keys('234567')
Select(find_element_medium('email', 'source')).select_by_value('DotDigital')
time.sleep(1)
Select(find_element_medium('email', 'sendname')).select_by_value('Community Education')
driver.execute_script("document.getElementById('emaildatesent').value = '2023-06-20'")  # it's read-only, so can't use send_keys
Select(find_element_medium('education', 'audience')).select_by_value('Teachers')
find_element_medium('education', 'creative').send_keys('Curriculum')
Select(find_element_medium('educationemail', 'linklocation1')).select_by_value('Image')
find_element_medium('educationemail', 'linkcontent1').send_keys('Sign Up')
url = final_url.get_attribute('value')
outputs['email'] += [url]

domain.clear()
domain.send_keys('https://www.redcrossfirstaidtraining.co.uk/courses/first-aid-legal-requirements/')
weird_dropdown('Red Cross Training_First aid', which='campaign')
Select(marketing_obj).select_by_value('Ecommerce purchase')
taxonomy_code.clear()
taxonomy_code.send_keys('234567')
Select(find_element_medium('email', 'source')).select_by_value('Salesforce')
time.sleep(1)
Select(find_element_medium('email', 'sendname')).select_by_value('Red Cross Training')
find_element_medium('training', 'audience').send_keys('B2B')
find_element_medium('training', 'creative').send_keys('Discount')
Select(find_element_medium('trainingemail', 'linklocation1')).select_by_value('Link')
find_element_medium('trainingemail', 'linkcontent1').send_keys('Sign Up')
url = final_url.get_attribute('value')
outputs['email'] += [url]

Select(find_element_medium('email', 'source')).select_by_value('Hubspot')
time.sleep(1)
Select(find_element_medium('trainingemail', 'linklocation1')).select_by_value('Button')
url = final_url.get_attribute('value')
outputs['email'] += [url]

#%% Internal

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Internal')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Yemen Crisis Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/yemen-crisis-appeal')
Select(find_element_medium('internal', 'source')).select_by_value('Homepage Herobox')
time.sleep(1)
find_element_medium('internal', 'linkdetails').send_keys('Test')
url = final_url.get_attribute('value')
outputs['internal'] = [url]

#%% Offline

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Offline')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Myanmar Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/myanmar-appeal')
Select(find_element_medium('offline', 'source')).select_by_value('Door Drop')
time.sleep(1)
Select(find_element_medium('offline', 'audience')).select_by_value('Cold Supporters')
find_element_medium('offline', 'linkdetails').send_keys('2019 01_URL winter')
url = final_url.get_attribute('value')
outputs['offline'] = [url]

Select(find_element_medium('offline', 'source')).select_by_value('Partially Addressed Mail')
url = final_url.get_attribute('value')
outputs['offline'] += [url]

#%% Rocketseed

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Rocketseed')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('UK Solidarity Fund', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/uk-solidarity-fund')
find_element_medium('rocketseed', 'linkdetails').send_keys('Sweet')
url = final_url.get_attribute('value')
outputs['rocketseed'] = [url]

weird_dropdown('Dance: Make Your Move', which='campaign')
domain.clear()
domain.send_keys('https://www.redcross.org.uk/get-involved/fundraising-and-events/dance-make-your-move')
Select(driver.find_element(By.CSS_SELECTOR, "#isIndividual")).select_by_value('No')
find_element_medium('rocketseed', 'linkdetails').clear()
find_element_medium('rocketseed', 'linkdetails').send_keys('Sign Up Now')
url = final_url.get_attribute('value')
outputs['rocketseed'] += [url]

#%% Referral

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Referral')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('Open Gardens', which='campaign')
domain.send_keys('www.redcross.org.uk/get-involved/fundraising-and-events/open-gardens')
find_element_medium('referral', 'source').send_keys('BBC')
Select(find_element_medium('referral', 'sourcecode')).select_by_visible_text('News or magazine site')
Select(find_element_medium('referral', 'adcreative')).select_by_visible_text('Article about us or our work')
url = final_url.get_attribute('value')
outputs['referral'] = [url]

#%% Unknown

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Unknown')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")

weird_dropdown('UK Fund Appeal', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/uk-crisis-appeal')
find_element_medium('other', 'audience').send_keys('Amadeus staff')
find_element_medium('other', 'linkdetails').send_keys('Support our work')
url = final_url.get_attribute('value')
outputs['unknown'] = [url]

#%% Other weird checks

driver.refresh()
Select(driver.find_element(By.CSS_SELECTOR, "#medium")).select_by_value('Audio')
time.sleep(1)

domain = driver.find_element(By.CSS_SELECTOR, "#domain")
final_url = driver.find_element(By.CSS_SELECTOR, "textarea#url")
marketing_obj = driver.find_element(By.CSS_SELECTOR, "#marketingobj")
taxonomy_code = driver.find_element(By.CSS_SELECTOR, "#taxonomycode")

weird_dropdown('Disaster Fund', which='campaign')
domain.send_keys('donate.redcross.org.uk/appeal/disaster-fund#:~:text=You%20can%20help%20people%20affected%20by%20disaster%20today&text=In%20any%20emergency%20%E2%80%93%20in%20the')

Select(marketing_obj).select_by_value('Donation')
taxonomy_code.send_keys('123456')
Select(find_element_medium('audio', 'source')).select_by_value('Spotify')
Select(find_element_medium('audio', 'adtype')).select_by_value('Interest')
find_element_medium('audio', 'adcreative').send_keys('CTA')
find_element_medium('audio', 'audience1').send_keys('Science nerds')

url = final_url.get_attribute('value')
outputs['other'] = [url]

find_element_medium('audio', 'adcreative').clear()
find_element_medium('audio', 'adcreative').send_keys('0---------1---------2---------3---------4---------5---------6---------7---------8---------9---------x')
url = final_url.get_attribute('value')
outputs['other'] += [url]

#%% Save dict

with open("checks\\generated_urls.json", "w") as outfile: 
    json.dump(outputs, outfile)

#%% Checks

driver.quit()

# Print for the check sheet
for k in ['video', 'audio', 'banner', 'socialad', 'socialpost', 'socialshare',
          'socialbutton', 'email', 'internal', 'offline', 'rocketseed',
          'referral', 'unknown', 'other']:
    for v in outputs[k]:
        print(v)
