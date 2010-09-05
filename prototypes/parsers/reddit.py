##Reddit Parser by flags/jetstar
#http://code.reddit.com/wiki/API#Rules

from parsers import BaseParser, BaseFeedItem
import feedparser

class RedditParser(BaseParser):
	#We'll replace $username later
	url='http://www.reddit.com/user/$username/.rss'
	
	def run(self):
		return_list = []
		feed = feedparser.parse(self.url.replace('$username',self.username))

		#print feed['feed']['title']
		for entry in feed['entries']:
			#Do some cleanup so we just return the actual title
			title=entry.title.replace(self.username+' on ','')
			#When
			timestamp=entry.date
			#Link
			link=entry.link
			item = BaseFeedItem(timestamp, title, link)
			return_list.append(item)
		
		return return_list