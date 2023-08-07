#! /usr/local/bin/python3
# -*- coding: utf-8 -*-

from .crawl_youtube import youtube_search
from .crawl_google_autocomplete import google_autocomplete
from .crawl_reddit import hot_topics
import argparse
import datetime

toRun = None
def log(message):
	"""Format logging"""

	timestamp = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S -")
	print(timestamp, message)

def now():
	"""Handy shorthand for execution time calculation"""

	now = datetime.datetime.utcnow()
	return now.isoformat()

def __callMe__():
	help_description = "Crawler to get search results from social media platforms."
	parser = argparse.ArgumentParser(description=help_description)
	parser.add_argument("-y", "--youtube-search", help="Perform youtube search. The search terms are stored in the configured MongoDB database", action="store_true")
	parser.add_argument("-g", "--google-autocomplete", help="Perform google autocomplete lookup base on search expressions stored in MongoDB database", action="store_true")
	parser.add_argument("-r", "--reddit-hot-topics", help="Gets Reddit 10 first hot topics", action="store_true")
	parser.add_argument("-i", "--input", help="Input file contining all the keyword to query for.", default="")
	args = parser.parse_args()
	if not args.input:
		log("[x] exiting; no input file provided.")
		exit()
	
	# catching start time to compute execution time
	begin_time = datetime.datetime.now()
	
	if args.youtube_search:
		log("[-] EXECUTING YOUTUBE RECO CRAWL " + "-"*10)
		toRun = youtube_search
	
	if args.google_autocomplete:
		log("[-] EXECUTING GOOGLE AUTOSUGGEST CRAWL " + "-"*10)
		toRun = google_autocomplete
	
	if args.reddit_hot_topics:
		log("[-] EXECUTING REDDIT CRAWL " + "-"*10)
		toRun = hot_topics
	
	with open(args.input) as inFile:
		queries = []
		for line in inFile:
			line = line.strip("\n")
			params = line.split(",")
			try:
				queries.append({
					"lang": params[0],
					"request_lang": params[1],
					"keyword": params[2]
				})
			except IndexError:
				log(f"[!] entry: {line} cannot be parsed; skipping.")
		log(f"[+] loaded {len(queries)} queires...")
		toRun(queries)
		# compute execution time
		exec_time = datetime.datetime.now() - begin_time
		log(f"[+] Execution time: {exec_time}")