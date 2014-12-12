'''
Pin-Scrape
https://github.com/Nateliason/pin-scrape

Overview:
This set of python functions will let you scrape anyone's public Pinterest Pinboards.
Its primary use is marketing/growth hacking... but get creative!
If you use this code for anything else, please keep the authors/contributors intact.
If you think of any improvements, go ahead and make them and submit a pull request. When you do, add your name here to the list of contributors.

Dependencies:
PyQuery: https://pythonhosted.org/pyquery/
FeedParser: https://pypi.python.org/pypi/feedparser

Thanks To:
Eristoddle at http://snipplr.com/view/64496/ for providing the code that most of this is based off of.
The [GrowthHackerTV](http://www.growthhacker.tv) community for being an inspiration to come up with things like this.

Contributors:
- Nathaniel Eliason @nateliason
- Vyacheslav Sukhenko @eternalfame
'''
from httplib import IncompleteRead
import urllib2

import feedparser
from pyquery import PyQuery as pq


def read_from_url(url):
    while True:  # fixes annoying IncompleteRead error when there are problems with internet connection
        try:
            content = urllib2.urlopen(url).read()
        except IncompleteRead:
            continue
        else:
            return content


def timeline(url): #gets the last 25 pins for a user or their pinboard depending on the URL you provide. 
    #pinterest.com/user/feed/rss for the user's most recent pins, /user/pinboard/rss for a certain pinboard. These pins can be fed in wherever you see "specific pin"
    #pinterest only stores 25 items in the feed... I'll see if there's any way to get more
    timeline = feedparser.parse(url)
    return (entry['id'] for entry in timeline['entries'])


def get_pinterest_timeline(user): #You can use this to get a user's feed if you just want to put in their Pinterest username
    return 'http://www.pinterest.com/%s/feed.rss' % user


def get_pinboard_timeline(user, board): #You can use this to get a user's feed if you just want to put in their Pinterest username
    return 'http://www.pinterest.com/%s/%s.rss' % (user, board)


def get_pinboards(user): #This won't get all of their pinboards necessarily. It'll get the pinboards for their last 25 pins. Still working on a better way to do this, but it's a start.
    pin_history = timeline(get_pinterest_timeline(user))
    boards = set()
    for url in pin_history:
        content = pq(read_from_url(url))
        board = content.find('meta[property="pinterestapp:pinboard"]').attr('content')
        if board not in boards:
            boards.add(board)
    print "Done getting pinboards"
    return boards


def item_url(specific_pin): #Takes the URL for a specific pin and gets the original URL for whatever was pinned. Useful for seeing what someone likes to pin from.
    try:
        content = pq(read_from_url(specific_pin))
        return content.find('meta[property="pinterestapp:source"]').attr('content')
    except:
        return None


def grab_pin(specific_pin): #You can use this to get a lot of the information from a specific pin of someone's.
    content = pq(read_from_url(specific_pin))
    og_keys = ('url', 'title', 'description', 'image')
    app_keys = ('pinboard', 'pinner', 'source', 'likes', 'repins', 'comments', 'actions')

    og_dict = {
        key: content.find('meta[property="og:%s"]' % key).attr('content') for key in og_keys
    }
    og_dict.update({
        key: content.find('meta[property="pinterestapp:%s"]' % key).attr('content') for key in app_keys
    })
    return og_dict


def get_urls(user): #Takes a user, gets their pinboards, then goes through those pinboards to find items that are from a certain URL
    pinboards = get_pinboards(user)

    for board in pinboards:
        board_name = board.split('/')[-2]  # as we know, the board variable content looks like
                                           # "pinterest.com/user/board/"
        board = get_pinboard_timeline(user, board_name)

        user_pins = timeline(board)

        for pin in user_pins:
            url = item_url(pin)
            if url is not None:
                yield url

        print "Done getting pins from board \"%s\"" % board_name