#packages
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
import time
import math

#-----------------------------------------------------
data = pd.read_excel('Biocheck_To Ghent_pigfarms_FI_2021_2022.xlsx', sheet_name= 'Data 2021')
offset = 21 #excel rij - 2, laatste getal in site, reeks die je wil toevoegen - 1
species = 'Pigs'
username = 'name@organisation.com'
password = 'password'
#----------------------------------------------------

# Open site
# open google driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome()

def inloggen():
    # officiele site
    driver.get('https://biocheckgent.com/en/user/login?destination=/en/dashboard')

    # test site
    # driver.get('https://biocheck.release.entityone.be/en/user/login')
    # time.sleep(5)

    #input credentials
    driver.find_element("id", "edit-name").send_keys(username, Keys.TAB, password, Keys.RETURN)

inloggen()

numberofrows = data.shape[0]

#exchange starting 6 with 8720 to have a way to differentiate between a radio button answer and a numeric answer starting in 6
def starts_with_6(number):
    return str(number).startswith(str('6'))

def starts_with_8720(number):
    return str(number).startswith(str('8720'))

def replace_starting_6_with_8720(number):
    return int('8720' + str(number)[1:])

for i in data.keys():
    if all(data[i].apply(starts_with_6)):
        data[i] = data[i].apply(replace_starting_6_with_8720)

#functions to click on the correct places in the site
def starting_clicks(titel):
    driver.find_element(By.LINK_TEXT, 'Surveys').click()
    driver.find_element(By.LINK_TEXT, species).click()
    driver.find_element(By.XPATH, '//*[@id="edit-submit"]').click()
    wait(driver, 7).until(EC.element_to_be_clickable((By.ID, 'edit-title-0-value'))).send_keys(titel, Keys.TAB, Keys.TAB, Keys.RETURN,
                                                               Keys.ARROW_DOWN * 81, Keys.RETURN)
    driver.find_element(By.ID, 'edit-field-permission-value').click()
    time.sleep(1.5)
    driver.find_element(By.ID, 'edit-submit').click()

def answer_radio(id):
    try:
        wait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id))).send_keys(Keys.SPACE)
    except TimeoutException:
        print('failed input')
        pass

def answer_num(id):
    try:
        wait(driver, 8).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + id))).send_keys(j)
    except TimeoutException:
        print('failed input')
        pass

#apply row by row

for i in range(1 + offset, numberofrows):
    #input is all answers for 1 biocheck
    input = data.values[i-1]
    titel = 'Automatic answer '+ '(' + str(i) + ') '  + str(input[0])
    input = input[1:]
    starting_clicks(titel)

    answercount = 0
    for j in input:
        if answercount in [10,26,48,55,64,70,76,80,88,94,100,112,119]:
            driver.find_element(By.ID, 'edit-next').click()
            print('newcat')

        if answercount > 118:
            time.sleep(5)

        print('\n', j)

        #3 options: radio buttons question, numeric question, no question

        #radio
        if starts_with_8720(j) or j == 'N' or j == 'Y':
            print('radio')
            if j == 'Y':
                choice = 1
            if j == 'N':
                choice = 2
            if j != 'N' and j != 'Y':
                choice = math.floor(j % 10)
            if choice != 9:
                id = 'edit-answer-' + str(answercount) + '-answer-' + str(choice)
                print(id)
                answer_radio(id)


        #numeric
        if (isinstance(j,int) or isinstance(j,float)) and not starts_with_8720(j) and not (j != j):
            print('numeric')
            print(answercount)
            id = 'edit-answer-' + str(answercount) + '-answer'
            print(id)
            answer_num(id)

        time.sleep(1.2)
        answercount += 1

    driver.find_element(By.ID, 'edit-next').click()
    wait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "[id^=" + 'edit-fictional-0'))).send_keys(Keys.SPACE)
    driver.find_element(By.ID, 'edit-next').click()
    driver.find_element(By.ID, 'edit-submit').click()
