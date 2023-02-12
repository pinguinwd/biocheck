# import necessary packages

import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
import openpyxl

#import excel file
data = pd.read_excel('data.xlsx',sheet_name='data')
vragen = pd.read_excel('data.xlsx',sheet_name='vragenlijst')

questionnaire = data.value.values[0]
taal = data.value.values[1]
helplink = data.value.values[2]

titels = vragen.Title.values
helpteksten = vragen.HelpText.values
Condtekst = vragen.ConditionalHelpText.values


#open google driver
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)

#officiele site
#driver.get('https://biocheckgent.com/en/user/login?destination=/en/dashboard')

#test omgeving
driver.get('https://biocheck.release.entityone.be/en/user/login')

time.sleep(5)

search = driver.find_element("id","edit-name")
search.send_keys("wannes.dewulf@ugent.be",Keys.TAB,'wannes.dewulf12',Keys.RETURN)

search = driver.find_element(By.LINK_TEXT, "Content")
search.click()

search = driver.find_element(By.LINK_TEXT,questionnaire)
search.click()

search = driver.find_element(By.LINK_TEXT, "Edit")
search.click()

search = driver.find_element(By.LINK_TEXT, "Questionnaire")
search.click()

#aanpassen van de titels
#TitelsVeranderen(titels, taal,PATH)

l = len(titels)
for i in range(l):
    vertaalknopID = "".join(['edit-field-q-questions-questions-',str(i),'-translate'])
    search = driver.find_element(By.ID, vertaalknopID).click()
    search =driver.find_element(By.XPATH, "".join(['//a[@hreflang=','"',taal,'"',']'])).click()
    search = driver.find_element(By.LINK_TEXT,'Edit').click()
    search = driver.find_element(By.ID, 'edit-delete-translation').click()
    search = driver.find_element(By.ID, 'edit-submit').click()
#aanpassen help teksten



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
