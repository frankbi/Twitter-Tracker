#!/usr/bin/env python

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys
import csv
import re
import os

def init(ss):
	if not os.path.exists("data"):
		os.makedirs("data")
	with open(ss, "r") as datafile:
		datas = csv.reader(datafile, delimiter="\t")
		for row in datas:
			usrdata = scrapeFollow(row[0], row[1])
			filename = "data/" + row[0] + ".tsv"
			if not os.path.exists(filename):
				with open(filename, "a") as newfile:
					newfile.write("DATE\tTIME\tNAME\tUSERNAME\tTWEETS\tFOLLOWERS\tFOLLOWING\n")
					newfile.write(usrdata)				 
			else:
				with open(filename, "a") as existingfile:
					existingfile.write(usrdata)

def	scrapeFollow(name, handle):
	r = requests.get("http://twitter.com/" + handle)
	soup = BeautifulSoup(r.text)

	numTweets = soup.findAll("a", {"data-element-term":"tweet_stats"})
	tweets = numTweets[0].find("strong")

	numFollowers = soup.findAll("a", {"data-element-term":"follower_stats"})
	followers = numFollowers[0].find("strong")

	numFollowing = soup.findAll("a", {"data-element-term":"following_stats"})
	following = numFollowing[0].find("strong")

	date = datetime.now().strftime('%Y-%m-%d')
	time = datetime.now().strftime('%H:%M')

	return date + "\t" + time + "\t" + name  + "\t" + handle + "\t" + reTweet(tweets) + \
			"\t" +reTweet(followers) + \
			"\t" + reTweet(following) + "\n"

def reTweet(string):
	string = str(string)
	match = re.search("title", string)
	if match:
		result = re.sub("<strong title=\"|\">(.*)$", "", string)
	else:
		result = re.sub("<strong>|</strong>", "", string)
	return result

if len(sys.argv) < 2:
	print "Please pass along a valid spreadsheet"
else:
	init(sys.argv[1])
