# import necessary packages

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from selenium.webdriver.common.action_chains import ActionChains
import numpy as np

#import excel file
data = pd.read_excel('data.xlsx',sheet_name='data')
vragen = pd.read_excel('data.xlsx',sheet_name='vragenlijst')

questionnaire = data.value.values[0]
taal = data.value.values[1]
helplinkoud = data.value.values[2]
helplinknieuw = data.value.values[3]

titels = vragen.Title.values
helpteksten = vragen.HelpText.values
descriptions = vragen.Description.values
Condtekst = vragen.ConditionalHelpText.values



#open google driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#officiele site
#driver.get('https://biocheckgent.com/en/user/login?destination=/en/dashboard')

#test omgeving
driver.get('https://biocheck.release.entityone.be/en/user/login')

time.sleep(5)

driver.find_element("id","edit-name").send_keys("wannes.dewulf@ugent.be",Keys.TAB,'wannes.dewulf12',Keys.RETURN)

driver.find_element(By.LINK_TEXT, "Content").click()

driver.find_element(By.LINK_TEXT, "Automatisation test").click()

driver.find_element(By.LINK_TEXT, "Edit").click()

driver.find_element(By.LINK_TEXT, "Questionnaire").click()

#aanpassen van de titels
#TitelsVeranderen(titels, taal,PATH)

l = len(titels)
for i in range(l):
    vertaalknopID = "".join(['edit-field-q-questions-questions-',str(i),'-translate'])
    driver.find_element(By.ID, vertaalknopID).click()
    driver.find_element(By.XPATH, "".join(['//a[@hreflang=','"',taal,'"',']'])).click()
    driver.find_element(By.ID, 'edit-name-0-value').clear()

    #edit titel
    if driver.find_elements(By.ID, 'edit-name-0-value'):
        vertaling = titels[i]
        driver.find_element(By.ID, 'edit-name-0-value').send_keys(vertaling)

    #edit description
    tekst = descriptions[i]
    elem = driver.find_elements(By.ID, 'edit-description-wrapper')
    if bool(elem):
        elem = driver.find_element(By.ID, 'edit-description-wrapper')
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem,10,10)
        action.click()
        action.key_down(Keys.CONTROL)
        action.send_keys('a')
        action.key_up(Keys.CONTROL)
        action.send_keys(Keys.BACKSPACE)
        action.send_keys(tekst)
        action.perform()

    #edit link
    search = driver.find_elements(By.ID, 'edit-report-link-0-uri')
    if bool(search):
        search = driver.find_element(By.ID, 'edit-report-link-0-uri')
        link = search.get_attribute('value')
        nieuwelink = link.replace(helplinkoud, helplinknieuw)
        search.clear()
        search.send_keys(nieuwelink)

    #edit help tekst
    tekst = helpteksten[i]
    elem = driver.find_elements(By.ID, 'edit-help-wrapper')
    if bool(elem):
        elem = driver.find_element(By.ID, 'edit-help-wrapper')
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem,10,10)
        action.click()
        action.key_down(Keys.CONTROL)
        action.send_keys('a')
        action.key_up(Keys.CONTROL)
        action.send_keys(Keys.BACKSPACE)
        action.send_keys(tekst)
        action.perform()

    #edit help link
#    search = driver.find_elements(By.ID, 'edit-help-link-0-uri')
#    if bool(search):
#        search = driver.find_element(By.ID, 'edit-help-link-0-uri')
#        link = search.get_attribute('value')
#        nieuwelink = link.replace(helplinkoud, helplinknieuw)
#        search.clear()
#        search.send_keys(nieuwelink)

    #edit cond tekst
    tekst = Condtekst[i]
    elem = driver.find_elements(By.ID, 'edit-conditional-help-wrapper')
    if bool(elem):
        elem = driver.find_element(By.ID, 'edit-conditional-help-wrapper')
        action = ActionChains(driver)
        action.move_to_element_with_offset(elem,10,10)
        action.click()
        action.key_down(Keys.CONTROL)
        action.send_keys('a')
        action.key_up(Keys.CONTROL)
        action.send_keys(Keys.BACKSPACE)
        action.send_keys(tekst)
        action.perform()

    #edit answers
    teller = 0
    antwoord = vragen.iloc[i, teller + 4]
    while isinstance(antwoord,str):
        antwoord = vragen.iloc[i, teller + 4]
        identity = 'edit-field-potential-answers-' + str(teller) + '-value'
        search = driver.find_element(By.ID, identity)
        search.clear()
        search.send_keys(antwoord)
        teller += 1
        antwoord = vragen.iloc[i, teller + 4]


    #submit
    driver.find_element(By.ID, 'edit-submit').click()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
