import requests
import scraperwiki
from datetime import datetime
from datetime import timedelta
import json
import time
import os

token = os.environ['fb_token']

with open("politicians.json") as json_file:
	politicians = json.load(json_file)
	
dateScraped = datetime.strftime(datetime.now(), '%Y-%m-%d')
initialSinceDate = '2013-01-01'
queryCount = 0
timeStarted = datetime.now()
windowEnd = datetime.now() + timedelta(hours=1)
print timeStarted, windowEnd


if scraperwiki.sqlite.get_var('upto'):
	upto = scraperwiki.sqlite.get_var('upto')
	print "Scraper upto:",upto
else:
	print "Scraper first run"
	upto = 0   

# upto = 0      

def getPosts(pageID,since):
	query = 'https://graph.facebook.com/v2.6/{pageID}/posts?limit=100&since={since}&access_token={token}'.format(pageID=pageID,token=token,since=since)
	global queryCount
	queryCount += 1
	results = requests.get(query)
	resultsJson = results.json()
	# handle errors
	
	if 'error' in resultsJson:
		print resultsJson['error']
	
	# no errors, so save data from first page of results
	
	else:
		# print resultsJson
		# save the data
		
		for result in resultsJson['data']:
			print result
			data = {}
			if 'message' in result:
				data['message'] = result['message']
			else:
				data['message'] = ''

			if 'story' in result:
				data['story'] = result['story']
			else:
				data['story'] = ''	

			data['createdTime'] = result['created_time']
			data['postID'] = result['id']
			data['pageID'] = pageID
			scraperwiki.sqlite.save(unique_keys=["pageID","createdTime","postID"], data=data)


	# check if more pages
	
	while 'paging' in resultsJson:

		# check if we have queries left

		while queryCount == 199:
			print "Waiting..."
			while windowEnd >= datetime.now():
				time_difference = windowEnd - datetime.now()
				print str(time_difference), ' to go'
				time.sleep(60)
			queryCount = 0 

		else:	
			results = requests.get(resultsJson['paging']['next'])
			queryCount += 1
			resultsJson = results.json()
			# print resultsJson
			
			for result in resultsJson['data']:
				print result
				data = {}
				if 'message' in result:
					data['message'] = result['message']
				else:
					data['message'] = ''

				if 'story' in result:
					data['story'] = result['story']
				else:
					data['story'] = ''	
					
				data['createdTime'] = result['created_time']
				data['postID'] = result['id']
				data['pageID'] = pageID
				scraperwiki.sqlite.save(unique_keys=["pageID","createdTime","postID"], data=data)


# for x in xrange(upto, len(politicians)):
for x in xrange(upto, len(politicians)):
	while queryCount == 199:
		print "Waiting..."
		while windowEnd >= datetime.now():
			time_difference = windowEnd - datetime.now()
			print str(time_difference), ' to go'
			time.sleep(60)
		queryCount = 0    

	else:	
		getPosts(politicians[x]['pageID'],initialSinceDate)

	scraperwiki.sqlite.save_var('upto', x)	 


