#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

import requests
from unidecode import unidecode as ud
import json
from bson import json_util
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import urllib.parse
import time

headers = { 
	"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0"
}

def log(message):
	""" Format logging """

	timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S -")
	print(timestamp, message)

def driver_init(url, language):
	""" Initialising driver """

	options = webdriver.ChromeOptions()
	options.add_argument("-headless")
	options.add_experimental_option("prefs", {"intl.accept_languages": language})
	options.add_argument("window-size=1366x768")

	driver = webdriver.Chrome(options=options)
	driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": headers["User-Agent"]})
	log("----------------- Connecting to: " + url)
	driver.get(url)

	return driver
	
def crawl_hot_topics(subreddit, lang):
	url = f"https://www.reddit.com/r/{subreddit}"
	driver = driver_init(url , lang)
	if not driver:
		return []
	wait = WebDriverWait(driver, 0)

	topics = driver.find_elements(By.XPATH, '//div[@data-testid="post-container"]')
	topic_list = []
	for i, details in enumerate(topics):
		ID = details.get_attribute("id")
		likes = details.find_element(By.XPATH, f"//*[@id=\"vote-arrows-{ID}\"]").text
		author = details.find_elements(By.XPATH, '//a[@data-testid="post_author_link"]')[i].text.split("/")[-1]
		scrapedAt = int(datetime.datetime.utcnow().timestamp())
		timestampShift = details.find_elements(By.XPATH, '//span[@data-testid="post_timestamp"]')[i].text
		_numComments = details.find_elements(By.XPATH, '//a[@data-click-id="comments"]')[i].text.split()
		numComments = _numComments[0] if len(_numComments) else ""
		permalink = details.find_elements(By.XPATH, '//a[@data-click-id="body"]')[i].get_attribute("href")
		title = details.find_elements(By.XPATH, '//div[@data-adclicklocation="title"]')[i].text.split("\n")[0]

		topic_list.append({
			"ID": ID,
			"NumLikes": likes,
			"Author": author,
			"NumComments": numComments,
			"PermaLink": permalink,
			"Title": title,
			"ScrapedAt": scrapedAt,
			"TimestampShift": timestampShift
		})
	log(f"Got {len(topic_list)} hot topics for {subreddit}")
	return {subreddit: topic_list}


def hot_topics(queries):

	for q in queries:
		lang = q["lang"]
		keyword = q["keyword"]
		request_lang = q["request_lang"]
		result = crawl_hot_topics(keyword, lang=f"{lang}, {request_lang}")
		if result:
			with open(f"{int(time.time())}_reddit_hot_topics_{keyword}_{request_lang}.json", "w") as oFile:
				oFile.write(json.dumps(result, indent=4))