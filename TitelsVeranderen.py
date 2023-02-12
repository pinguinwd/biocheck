def TitelsVeranderderen(titels,taal,PATH):

    l = len(titels)
    for i in range(l):
        vertaalknopID = "".join(['edit-field-q-questions-questions-',str(i),'-translate'])
        search = driver.find_element(By.ID, vertaalknopID).click()
        search =driver.find_element(By.XPATH, "".join(['//a[@hreflang=','"',taal,'"',']'])).click()
        search = driver.find_element(By.ID, 'edit-name-0-value').clear()
        vertaling = titels[i]
        driver.find_element(By.ID, 'edit-name-0-value').send_keys(vertaling)
        search = driver.find_element(By.ID, 'edit-submit').click()