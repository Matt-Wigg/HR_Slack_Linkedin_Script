# ----- Imports ------ #

import random
import re
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
from secrets import username, password

# -------------------- #

# -- Path to chromedriver -- #
browser = webdriver.Chrome("*** CHROMEDRIVER PATH HERE - EG: /Users/mpw/Desktop/LinkedIn Script/chromedriver ***")

# -- Global wait time for finding elements -- #
browser.implicitly_wait(4)

# -- Directs browser to LinkedIn home page -- #
browser.get('https://www.linkedin.com/')

linkdin_sign_in_btn = browser.find_element_by_xpath(
            "/html/body/nav/a[3]")
linkdin_sign_in_btn.click()

time.sleep(1)

# -- INPUTS USERNAME -- #
email_in = browser.find_element_by_id('username')
email_in.send_keys(username)

# -- INPUTS PASSWORD -- #
password_in = browser.find_element_by_id('password')
password_in.send_keys(password, Keys.ENTER)

time.sleep(1)

# hack reactor emails #
target_file = 'HR_Slack_Copy.txt'

# Open the target file in Read mode
target_open = open(target_file, 'r')

# Read the text from the file
text = target_open.read()

profileQueued = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-?=%.]+', text)
visitedProfile = []

time.sleep(1)

error_count = 0
success_count = 0
while len(profileQueued) > 0:
    try:
        visitingProfileID = profileQueued.pop()
        visitedProfile.append(visitingProfileID)
        fullLink = visitingProfileID
        browser.get(fullLink)

        close_messager = browser.find_element_by_class_name('msg-overlay-bubble-header')
        close_messager.click()

        browser.find_element_by_class_name(
            'pv-s-profile-actions__overflow').click()

        browser.find_element_by_class_name(
           'pv-s-profile-actions--connect').click()

        browser.find_element_by_class_name('mr1').click()

        contact_name = BeautifulSoup(
            browser.page_source, features="html.parser").find('h2', id='send-'
                                                              'invite-modal')
        contact_name = str(contact_name).split()
        custom_message = "Hello, {}.\n\nI am a fellow Hack Reactor student!".format(str(contact_name[3]))
        element_ID = browser.find_element_by_id('custom-message')
        element_ID.send_keys(custom_message)

        browser.find_element_by_class_name('ml1').click()

        with open('Visited_users_list.txt', 'a') as visited_user_file:
            visited_user_file.write(str(visitingProfileID) + '\n')
        visited_user_file.close()

        success_count += 1

        print("Success {}: profile '{}' has been contacted.".format(str(
            success_count), str(visitedProfile[-1])))

        time.sleep(random.uniform(3, 12))

        if len(visitedProfile) % 10 == 0:
            print('Visited Profiles: ', len(visitedProfile))
    except Exception:
        error_count += 1
        print("Error {}: profile '{}' has no contact option."
              .format(str(error_count), str(visitedProfile[-1])))

print('Script complete.\nTotal Visited Profiles =', len(visitedProfile))
print('Total Successes =', str(success_count))
print('Total Errors =', str(error_count))
