import pandas as pd
from selenium import webdriver
import numpy as np
import datetime
import schedule
import time

import fbchat
from fbchat import Client
from fbchat.models import *

def send_reminder():

    #URL of all grade sections of canvas, and URL of messenger chat to send it to
    classes_people = [("url","messenger url")]
    
    #Canvas username and password stored in a file and read
    f = open("")
    username = f.readline().replace("\n","")
    password = f.readline()
    f.close()

    months = {"Sep": 9, "Oct":10, "Nov":11, "Dec":12}

    #Log into facebook in order to send messages
    file = open("")
    email = file.readline().replace("\n","")
    pw = file.readline()
    file.close()

    client = Client(email,pw)


    #Log into portal so you can access canvas in another tab
    #need access to chrom driver
    driver = webdriver.Chrome("chromedriver_win32/chromedriver.exe")

    #url to log into the account the first time
    url = " "

    driver.get(url)

    driver.find_element_by_id("j_username").send_keys(username)
    driver.find_element_by_id("j_password").send_keys(password)
    driver.find_element_by_id("btn-eventId-proceed").click()

    #loops through each url and group message
    for Class, chatID in classes_people:

        #loads the grades page and grabs the grades dataframe 
        driver.get(Class)
        html = driver.page_source
        d = pd.read_html(html)

        grades = d[0]

        for num in range(len(grades)):
            #check to make sure its not empty
            if type(grades.loc[num][1]) == str:
                #gets each assignments due date
                ass_date = grades.loc[num][1].split(" ")[:2]
                ass_month = months[ass_date[0]]
                try:
                    ass_day = int(ass_date[1])
                except ValueError:
                    ass_day = int(ass_date[1].strip().replace(",",""))
                
                #gets the current assingment due date
                curr_month = datetime.datetime.now().month
                curr_day = datetime.datetime.now().day

                #checks if due date is equal to today's date
                if curr_day == ass_day and curr_month == ass_month:
                    ass = grades.loc[num][0]
                    time = " ".join(grades.loc[num][1].split(" ")[2:])

                    #string to be sent
                    messageString = "{0} due {1}".format(ass, time)
                    
                    #sends message
                    client.send(Message(text=messageString), thread_id=chatID, thread_type=ThreadType.GROUP)

send_reminder()
#change time to any
schedule.every().day.at("18:23").do(send_reminder)

while True:
    schedule.run_pending()
    time.sleep(1)