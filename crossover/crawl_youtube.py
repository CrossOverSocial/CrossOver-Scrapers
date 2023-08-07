#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from pymongo import MongoClient
import re
import json
from bson import json_util
import datetime, time
import requests
import youtube_dl
from youtube_dl.utils import DownloadError
from youtube_dl.utils import ExtractorError
import traceback
import urllib.parse
import urllib3
from random import randint
from time import sleep, time
import os
import subprocess


ydl_params = {"quiet": True}
ydl = youtube_dl.YoutubeDL(ydl_params)

ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

begin_time = datetime.datetime.now()

yt_base_url = "https://www.youtube.com"
browserLang = ""

headers = { 
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36" 
}

options = webdriver.ChromeOptions()
options.add_argument("-headless")
options.add_experimental_option("prefs", {"intl.accept_languages": browserLang})
options.add_argument("window-size=1366x768")

def kill_old():
    SubProcess = subprocess.Popen(["ps", "-A"], stdout=subprocess.PIPE)
    output, error = SubProcess.communicate()
    target_process = "python3 crossover.py -y"
    for line in output.splitlines():
        if target_process in str(line):
            pid = int(line.split(None, 1)[0])
            os.kill(pid, 9)

def log(message):
    timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S -")
    print(timestamp, message)

def wait_XPATH_SELECTOR(driver, condition, timeout=20, retries=20):
    """ Instucts the WebDriver to wait until a specific condition is met """

    wait = WebDriverWait(driver, timeout)
    retry_count = 1
    while retry_count <= retries:
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, condition)))
            break
        except TimeoutException:
            log(f"Connection failed. Retrying... (Retry {retry_count} of {retries})")
            driver.refresh()
            retry_count += 1

def driver_init(url):
    """ initialising driver """

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 10)
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": headers["User-Agent"]})
    driver.get(url)
    log(f"----------------- Connecting to: {url}")
    return driver, wait

def random_wait(min, max):
    delay = randint(min, max)
    log(f"Applying {delay} seconds delay before next request...")
    sleep(delay)

def get_recommended_videos_from_search(driver):
    """ gets a webdriver element containing the list of search results on a typical youtupe page `https://www.youtube.com/?results&search_query= """
    videosSelector = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer"
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.XPATH, videosSelector)))
    videos = driver.find_elements(By.XPATH, videosSelector)

    video_links = []

    for i, video in enumerate(videos):
        try:
            vid_url_element = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            vid_url = video.find_element(By.TAG_NAME, "a").get_attribute("href").split("pp")[0]
            video_links.append(vid_url)
        except StaleElementReferenceException:
            log("Stale Element. Passing...")

    return video_links

def get_recommended_videos_from_url(driver):
    """gets a webdriver element containing the list of search results on a typical youtupe page `https://www.youtube.com/?results&search_query="""

    log("waiting recos")
    wait_condition = "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[4]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer"
    wait_XPATH_SELECTOR(driver, wait_condition)
    videos = driver.find_elements(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[4]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer")
    log("Got list of recommended videos")

    video_links = []

    for i, video in enumerate(videos):
        try:
            vid_url_element = WebDriverWait(driver, 20, ignored_exceptions=ignored_exceptions).until(EC.presence_of_element_located((By.TAG_NAME, "a")))
            vid_url = video.find_element(By.TAG_NAME, "a").get_attribute("href")
            video_links.append(vid_url)
        except StaleElementReferenceException:
            log("Stale Element. Passing...")

    return video_links

def accept_conditions(driver):
    """takes a selenium driver instance as argument and accepts the video pop-up to get rid of it for clean screenshots when using a new user profile"""

    log("Accepting conditions")
    driver.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]").click()
    wait_condition = "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[2]"
    wait_XPATH_SELECTOR(driver, wait_condition)
    log("Conditions successfully accepted")

def get_vid_metadata(yt_url):
    """parses ytdl output and forms a dict"""

    try:
        log(f'Getting metadata for {yt_url}')
        ydl_out = ydl.extract_info(yt_url, download=False)

        vid_metadata = {
            "id": ydl_out.get("id"),
            "title": ydl_out.get("title"),
            "thumbnails": ydl_out.get("thumbnails"),
            "description": ydl_out.get("description"),
            "upload_date": ydl_out.get("upload_date"),
            "uploader": ydl_out.get("uploader"),
            "uploader_id": ydl_out.get("uploader_id"),
            "uploader_url": ydl_out.get("uploader_url"),
            "channel_id": ydl_out.get("channel_id"),
            "channel_url": ydl_out.get("channel_url"),
            "duration": ydl_out.get("duration"),
            "view_count": ydl_out.get("view_count"),
            "average_rating": ydl_out.get("average_rating"),
            "age_limit": ydl_out.get("age_limit"),
            "webpage_url": ydl_out.get("webpage_url"),
            "categories": ydl_out.get("categories"),
            "tags": ydl_out.get("tags"),
            "is_live": ydl_out.get("is_live"),
            "like_count": ydl_out.get("like_count"),
            "channel": ydl_out.get("channel")
        }
        return vid_metadata 

    except DownloadError as e:
        log("Skipping +18 video")

def get_yt_videos(query, lang):
    results = {query: []}

    url = f"{yt_base_url}/results?search_query={urllib.parse.quote(query)}"
    reload_counter = 0
    while reload_counter < 9:
        try:
            chrome, wait = driver_init(url)
            wait_cond = EC.presence_of_element_located((By.CSS_SELECTOR, "#contents > ytd-video-renderer:nth-child(19)"))
            wait.until(wait_cond)
            if reload_counter >= 1:
                log(f"{reload_counter} retrie(s)")
            reload_counter = 9
        except KeyboardInterrupt:
            exit()
        except:
            reload_counter += 1
            log(f"Connection lost, retry {reload_counter} of 10" + traceback.format_exc())

    accept_conditions(chrome)
    video_links = get_recommended_videos_from_search(chrome)

    for i, link in enumerate(video_links):
        try:
            vid_metadata = get_vid_metadata(link)
            results[query].append(vid_metadata)
        except KeyboardInterrupt:
            chrome.quit()
            exit()
        except:
            log("Connection lost" + traceback.format_exc())

    log(f"Getting recommendations for each {len(video_links)} search results...")

    for i, item in enumerate(results[query]):
        reload_counter = 0
        reload_attempts = 5
        failed = False
        while reload_counter < reload_attempts:
            try:
                chrome, wait = driver_init(item["webpage_url"])
                wait_cond = EC.presence_of_element_located((By.CSS_SELECTOR, "#items > ytd-compact-video-renderer:nth-child(19)"))
                wait.until(wait_cond)
                if reload_counter >=1:
                    log(f"{reload_counter} retrie(s)")
                reload_counter = reload_attempts
            except TimeoutException as e:
                chrome.quit()
                log(f"Timeout, quitting and relaunching browser. Attempt {reload_counter + 1} of 5")
                log(e)
                time.sleep(2)
                if reload_counter == reload_attempts -1:
                    reload_counter +=1
                    failed = True
                else:
                    reload_counter +=1
                    log(f"reload_counter: {reload_counter}")
            except TypeError:
                pass
            except KeyboardInterrupt:
                chrome.quit()
                exit()
            except:
                log("Connection lost, retrying" + traceback.format_exc())
                chrome.quit()
                if reload_counter <= reload_attempts:
                    reload_counter +=1
                else:
                    failed = True
        if not failed:
            recos = get_recommended_videos_from_url(chrome)
            item["recos"] = []
            for reco_link in recos:
                reco_metadata = get_vid_metadata(reco_link)
                item["recos"].append(reco_metadata)
            chrome.quit()
        else:
            log("Too may retries, aborting")
            chrome.quit()

    return results

def youtube_search(queires):
    kill_old()
    
    for q in queires:
        lang = q["lang"]
        keyword = q["keyword"]
        request_lang = q["request_lang"]
        results = get_yt_videos(keyword, f"{lang}, {request_lang}")
        with open(f"{int(time())}_youtube_search_{keyword}_{request_lang}.json", "w") as oFile:
            oFile.write(json.dumps(results, indent=4))