#!/usr/local/bin/python 

import sys, os
import re
from ConfigParser import SafeConfigParser
import praw
import time
#from log_conf import LoggerManager

containing_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
cfg_file = SafeConfigParser()
path_to_cfg = os.path.join(containing_dir, 'config.cfg')
cfg_file.read(path_to_cfg)

username = cfg_file.get('reddit', 'username')
password = cfg_file.get('reddit', 'password')
app_key = cfg_file.get('reddit', 'app_key')
app_secret = cfg_file.get('reddit', 'app_secret')
subreddit = cfg_file.get('reddit', 'subreddit')
curr_id = cfg_file.get('confirm', 'link_id')

#logger=LoggerManager().getLogger(__name__)

def get_month():
	month = time.strftime('%B')
	return(month)

def login():
	r = praw.Reddit(client_id=app_key,
                     client_secret=app_secret,
                     username=username,
                     password=password,
                     user_agent=username)
     	return(r)
def post_thread(r,month):
	post = r.subreddit(subreddit).submit('%s Confirmed Trade Thread' % month, selftext='''Post your confirmed trades below,

* Only the original seller or trader(The one that put up the post) should post and the buyer/trader should only comment. Only one trade confirmation per comment

* For WTS posts the seller needs to say "*sold*" and the receivers username somewhere in the comment. example "*sold a knife to /u/username*"
* For WTT posts the original trader needs to say "*Traded*" and the receivers username somewhere in the comment. example "*Traded knives with /u/username*"
* When confirming a post put "*Confirmed*" only nothing else it makes the bot unhappy :(


If more proof is requested by the bot please send a [modmail](http://www.reddit.com/message/compose?to=%%2Fr%%2F%s) including the following:

* Screenshot of PM\'s between the users
* Permalink to trade confirmed thread comment

#Make sure to only confirm when you have recived the knife!


# Any attempts to game the system or to scam will result in a swift and permanent ban
''' % subreddit, send_replies=False)

	post.mod.distinguish()
     	#post.mod.sticky(bottom=True)
     	post.mod.suggested_sort(sort='new')
	#post.sticky(bottom=False)
	#r.send_message('/r/'+subreddit, 'New Trade Thread', 'A new trade thread has been posted for the month and the sidebar has been updated.')
	return (post.id)

def change_sidebar(r, post_id, month):
	sb = r.subreddit(subreddit).mod.settings()["description"]
	new_flair = r'[Confirm Your Trades](/' + post_id + ')'
	print post_id
	new_sb = re.sub(r'\[Confirm Your Trades\]\(\/[a-z0-9]+\)',new_flair, sb, 1)
	r.subreddit(subreddit).mod.update(description=new_sb)

def update_config(post_id):
	cfg_file.set('confirm', 'prevlink_id', curr_id)
	cfg_file.set('confirm', 'link_id', post_id)
	with open(r'config.cfg', 'wb') as configfile:
		cfg_file.write(configfile)

def main():
	month = get_month()
	r = login()
	post_id = post_thread(r, month)
	change_sidebar(r, post_id, month)
	update_config(post_id)
	#logger.info("Posted Trade Confirmation thread")

if __name__ == '__main__':
	main()
