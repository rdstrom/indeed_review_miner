import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

#drivers
from selenium import webdriver
import chromedriver_binary  # Adds chromedriver binary to path
from selenium.webdriver.common.by import By

driver = webdriver.Chrome('C:/Users/SFPC/Downloads/chromedriver_win32/chromedriver.exe')
driver.get("https://www.indeed.com/cmp/John-Deere/reviews")
#extract lists of elements

review_title = review_sub_date = driver.find_elements(By.CLASS_NAME, 'cmp-Review-title')
review_author = review_sub_date = driver.find_elements(By.CLASS_NAME, 'cmp-ReviewAuthor')
review_body = review_sub_date = driver.find_elements(By.CLASS_NAME, 'cmp-NewLineToBr-text')
