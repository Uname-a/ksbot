#!/usr/local/bin/python


import sys, os
import re
from ConfigParser import SafeConfigParser
import praw
from datetime import datetime as dt
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

#logger=LoggerManager().getLogger(__name__)
def suffix(d):
    return 'th' if 11<=d<=13 else {1:'st',2:'nd',3:'rd'}.get(d%10, 'th')

def custom_strftime(format, t):
    return t.strftime(format).replace('{S}', str(t.day) + suffix(t.day))

def login():
	r = praw.Reddit(client_id=app_key,
                     client_secret=app_secret,
                     username=username,
                     password=password,
                     user_agent=username)
     	return(r)
def post_thread(r,date):
	post = r.subreddit(subreddit).submit('Want To Buy Thread -  %s' % date.upper(), selftext='''This is the official [WTB] thread for /r/%s! The rules are simple:

* List what specific items you want. The more info the better
* List what you have to offer 
* **This is not a sales thread
* As always be careful

''' % subreddit, send_replies=False)
	post.mod.distinguish()
	post.mod.sticky(bottom=True)
	post.mod.suggested_sort('new')
	#r.send_message('/r/'+subreddit, 'New Trade Thread', 'A new trade thread has been posted for the month and the sidebar has been updated.')
	return (post.id)

def change_sidebar(r, post_id):
	sb = r.subreddit(subreddit).mod.settings()["description"]
	new_flair = r'[WTB Thread](/' + post_id + ')'
	new_sb = re.sub(r'\[WTB Thread\]\(\/[a-z0-9]+\)',new_flair, sb, 1)
	r.subreddit(subreddit).mod.update(description=new_sb)

def update_config(post_id):
	cfg_file.set('price', 'WTB', post_id)
	with open(r'config.cfg', 'wb') as configfile:
		cfg_file.write(configfile)

def main():
	date = custom_strftime('%B {S}', dt.now())
	r = login()
	post_id = post_thread(r, date)
	change_sidebar(r, post_id)
	update_config(post_id)
	#logger.info("Posted Price Check thread")
	
if __name__ == '__main__':
	main()
