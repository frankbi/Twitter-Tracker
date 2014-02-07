#!/usr/bin/python

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys
import csv
import re

def init():
	with open(sys.argv[1], "r") as csvfile:
		readit = csv.reader(csvfile, delimiter="\t")
		for row in readit:
			usrdata = scrapFollow(row[0], row[1])
			filename = "data/" + row[0] + ".csv"
			try:
				with open(filename) as datafile:
					datafile.write(usrdata)
			except IOError:
				with open(filename, "a") as newfile:
					newfile.write("DATE\tTIME\tNAME\tUSERNAME\tTWEETS\tFOLLOWERS\tFOLLOWING\n" + usrdata)

def	scrapFollow(name, handle):
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

init()
