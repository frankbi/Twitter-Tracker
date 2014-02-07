#!/usr/bin/python

from bs4 import BeautifulSoup
from datetime import datetime
import requests
import sys
import csv


def	scrapFollow():
	r = requests.get("http://twitter.com/" + sys.argv[1])
	soup = BeautifulSoup(r.text)

	numTweets = soup.findAll("a", {"data-element-term":"tweet_stats"})
	tweets = numTweets[0].find("strong")	

	numFollowers = soup.findAll("a", {"data-element-term":"follower_stats"})
	followers = numFollowers[0].find("strong").extract()

	numFollowing = soup.findAll("a", {"data-element-term":"following_stats"})
	following = numFollowing[0].find("strong")

	time = datetime.now().strftime('%H:%M')

	c = csv.writer(open("SOTU-STATS.csv", "a"))
	c.writerow([time, sys.argv[1], followers, following, tweets])

scrapFollow()
