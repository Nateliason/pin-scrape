'''
Pin-Scrape
https://github.com/Nateliason/pin-scrape

Overview:
This set of python functions will let you scrape anyone's public Pinterest Pinboards.
Its primary use is marketing/growth hacking... but get creative!
If you use this code for anything else, please keep the authors/contributors intact.
If you think of any improvements, go ahead and make them and submit a pull request. When you do, add your name here to the list of contributors.

Dependencies:
BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/
SoupSelect: https://code.google.com/p/soupselect/
FeedParser: https://pypi.python.org/pypi/feedparser

Thanks To:
Eristoddle at http://snipplr.com/view/64496/ for providing the code that most of this is based off of.
The [GrowthHackerTV](http://www.growthhacker.tv) community for being an inspiration to come up with things like this.

Contributors:
- Nathaniel Eliason @nateliason
'''

import urllib2
from bs4 import BeautifulSoup
from bs4 import BeautifulSoup as Soup
from soupselect import select
import feedparser



pinboards = [] #a collection of the user's pinboards. You can feed this back into timeline() to get more pins



def timeline(url): #gets the last 25 pins for a user or their pinboard depending on the URL you provide. 
	#pinterest.com/user/feed/rss for the user's most recent pins, /user/pinboard/rss for a certain pinboard. These pins can be fed in wherever you see "specific pin"
	#pinterest only stores 25 items in the feed... I'll see if there's any way to get more

	timeline = feedparser.parse(url)
	pins = []
	for i in range(0,len(timeline['entries'])):
		pins.append(timeline['entries'][i]['id'])
	return pins



def get_pinterest_timeline(user): #You can use this to get a user's feed if you just want to put in their Pinterest username
	return 'http://www.pinterest.com/' + user + '/feed/rss'



def get_pinboards(user): #This won't get all of their pinboards necessarily. It'll get the pinboards for their last 25 pins. Still working on a better way to do this, but it's a start.
	pin_history = timeline(get_pinterest_timeline(user))
	for i in pin_history:
		soup = BeautifulSoup(urllib2.urlopen(i).read())
		pinboard = select(soup, 'meta[property="pinterestapp:pinboard"]')[0]['content']
		if pinboard not in pinboards:
			pinboards.append(pinboard)
	print "Done getting pinboards"



def item_url(specific_pin): #This will take a specific pin's URL and give you the original URL for that content. Useful for figuring out where someone is pinning clothes from, for example.
	soup = BeautifulSoup(urllib2.urlopen(specific_pin).read())
	return select(soup, 'meta[property="pinterestapp:source"]')[0]['content']



def grab_pin(specific_pin): #You can use this to get a lot of the information from a specific pin of someone's.
    soup = BeautifulSoup(urllib2.urlopen(specific_pin).read())
    return {
        "url": select(soup, 'meta[property="og:url"]')[0]['content'],
        "title": select(soup, 'meta[property="og:title"]')[0]['content'],
        "description": select(soup, 'meta[property="og:description"]')[0]['content'],
        "image": select(soup, 'meta[property="og:image"]')[0]['content'],
        "pinboard": select(soup, 'meta[property="pinterestapp:pinboard"]')[0]['content'],
        "pinner": select(soup, 'meta[property="pinterestapp:pinner"]')[0]['content'],
        "source": select(soup, 'meta[property="pinterestapp:source"]')[0]['content'],
        "likes": select(soup, 'meta[property="pinterestapp:likes"]')[0]['content'],
        "repins": select(soup, 'meta[property="pinterestapp:repins"]')[0]['content'],
        "comments": select(soup, 'meta[property="pinterestapp:comments"]')[0]['content'],
        "actions": select(soup, 'meta[property="pinterestapp:actions"]')[0]['content'],
    }