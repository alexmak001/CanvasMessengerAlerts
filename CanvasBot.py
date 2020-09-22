import pandas as pd
from selenium import webdriver
import numpy as np

username = ""
password = ""

driver = webdriver.Chrome("chromedriver_win32/chromedriver.exe")

url = "https://myportal.fhda.edu"

driver.get(url)

driver.find_element_by_id("j_username").send_keys(username)
driver.find_element_by_id("j_password").send_keys(password)
driver.find_element_by_id("btn-eventId-proceed").click()


classes = [""]


driver.get(classes[0])
html = driver.page_source
d = pd.read_html(html)
grades = d[0].to_numpy()

for item in grades[0]:
    print(item)
