#!/usr/bin/env python
#coding=utf-8

import unicodecsv as csv
import sqlite3
import pandas.io.sql as sql
import re
import simplejson as json
import sentiment

results = []

usernamesFile = open("politicians.json")
usernames = json.load(usernamesFile)

for d,i in enumerate(usernames):
	print "checking", d['pageID']
	con = sqlite3.connect('scraperwiki.sqlite')
	query = 'select * from comments where pageID="{pageID}"'.format(pageID=d['pageID'])
	table = sql.read_sql(query, con)

	# print table

	rows = table.iterrows()

	abuseTweets = []
	for row in rows:
		sentimentResult = sentiment.getSentiment(row[1]['message'])
		print sentimentResult
		results.append({"pol_id":i,"partyCode":d["partyCode"],"gender":d["gender"],"message":row[1]['message'],"positive":sentimentResult['positive'],"negative":sentimentResult['negative'],"createdTime":row[1]['createdTime']})

	# print results
	with open('facebook-sentiment-test.csv', 'w') as csvoutput:
		dict_writer = csv.DictWriter(csvoutput, results[0].keys())
		dict_writer.writer.writerow(results[0].keys())
		dict_writer.writerows(results)	



