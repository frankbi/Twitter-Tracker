#!/usr/bin/python

from bs4 import BeautifulSoup
import requests
import sys

r = requests.get("http://twitter.com/" + sys.argv[1])
soup = BeautifulSoup(r.text)
followers = soup.findAll("a", {"data-element-term":"follower_stats"})
print "Followers: " + followers[0].find("strong").get_text()

following = soup.findAll("a", {"data-element-term":"following_stats"})
print "Following: " + following[0].find("strong").get_text()
