#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import re, json, time, datetime, requests
import urllib.parse

from bs4 import BeautifulSoup
from unidecode import unidecode as ud
from bson import json_util

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

headers = { 
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" 
}

def log(message):
	""" Format logging """

	timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S -")
	print(timestamp, message)

def driver_init(url, language):
	""" initialising driver """

	options = webdriver.ChromeOptions()
	options.add_argument("-headless")
	options.add_experimental_option("prefs", {"intl.accept_languages": language})
	options.add_argument("window-size=1366x768")

	driver = webdriver.Chrome(options=options)
	driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": headers["User-Agent"]})
	log("----------------- Connecting to: " + url)
	driver.get(url)
	return driver

	
def crawl_autosuggests(query, lang):
	lang = lang.split()[1]
	driver = driver_init(f"https://www.google.be/?hl={lang}", lang)
	wait = WebDriverWait(driver, 10)
	accept_button = driver.find_element(By.XPATH, "/html/body/div[2]/div[3]/div[3]/span[1]/div[1]/div[1]/div[1]/div[3]/div[1]/button[2]")
	driver.implicitly_wait(10)
	accept_button.click()
	wait.until(EC.invisibility_of_element_located(accept_button))
	query_box = driver.find_element(By.XPATH, '//textarea[@name="q"]')

	for q in query:
		query_box.send_keys(q)
	time.sleep(10)
	driver.save_screenshot(f"{int(time.time())}_google_autocomplete_{query}_{lang}.png")

	ac_container = driver.find_element(By.XPATH, '//ul[@role="listbox"]')
	ac_list = ac_container.find_elements(By.XPATH, '//li[@role="presentation"]')
	ac_as_text = []
	for i in ac_list:
		if i.text:
			ac_as_text.append(i.text.replace("\n", " "))
	results = {query: ac_as_text}
	return results

def google_autocomplete(queries):
	for q in queries:
		lang = q["lang"]
		keyword = q["keyword"]
		request_lang = q["request_lang"]
		with open(f"{int(time.time())}_google_autocomplete_{keyword}_{request_lang}.json", "w") as oFile:
			result = crawl_autosuggests(keyword, lang=f"{lang}, {request_lang}")
			oFile.write(json.dumps(result))
			log(f"Got {len(result[keyword])} for the keyword {keyword} - {request_lang}")
