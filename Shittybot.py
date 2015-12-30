import praw
import sqlite3 
import time

'''For logging using OAUTH. Dont really know what this does yet'''
app_ua = '/u/Jajoos thingamajig for personal SUbreddit'
app_id = 'k5HlkFU8FpneIA'
app_secret = 'tyh7XcnE3TkghIbc-Ee2TgPUjag'
app_uri = 'https://127.0.0.1:65010/authorize_callback'

r = praw.Reddit(app_ua)

app_scopes = 'account creddits edit flair history identity livemanage modconfig modcontributors modflair modlog modothers modposts modself modwiki mysubreddits privatemessages read report save submit subscribe vote wikiedit wikiread'

#https://www.reddit.com/api/v1/authorize/?response_type=code&client_id=k5HlkFU8FpneIA&state=...&duration=permanent&scope=account+creddits+edit+flair+history+identity+livemanage+modconfig+modcontributors+modflair+modlog+modothers+modposts+modself+modwiki+mysubreddits+privatemessages+read+report+save+submit+subscribe+vote+wikiedit+wikiread&redirect_uri=https%3A%2F%2F127.0.0.1%3A65010%2Fauthorize_callback'

app_account_code = 'T9rP13go2YKogi8vytP50QpPQ_s'
app_refresh = '43599436-NgzTYzkDRj08EnffOURkvCL7zOc'

SUBREDDIT = 'CNIMBB'
MAXPOSTS = 100
SETPHRASES = ['what is this?', 'confused', 'wtf', 'what is this sub']
SETRESPONSE = "Hello and Welcome to Chicken Nuggets in My Blue Bucket (CNIMBB)! Make sure to be eating chicken nuggets out of a (preferably) blue bucket while posting, commenting, or bitching about this sub. If you do not comply you will be banned by the glorious overlord, Jajoo (may he live long and prosper)"
USERNAME = "__Stanley__"

WAIT = 20

print("Opening Database")
sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS oldposts(id TEXT)')
sql.commit()

def login(r):
    r.set_oauth_app_info(app_id, app_secret, app_uri)
    r.refresh_access_information(app_refresh)
    return r
    print("Loggin In")

def replyBot(r):
    print('Grabbing subreddit ' + SUBREDDIT)
    subreddit = r.get_subreddit(SUBREDDIT)
    print('Fetching comments')
    comments = subreddit.get_comments(limit=MAXPOSTS)
    for comment in comments:
        cid = comment.id
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [cid])
        if not cur.fetchone():
            try:
                cauthor = comment.author.name
                if cauthor.lower() != USERNAME.lower():
                    cbody = comment.body.lower()
                    if any(key.lower() in cbody for key in SETPHRASES):
                        print('Replying to ' + cauthor)
                        comment.reply(SETRESPONSE)
            except AttributeError:
                pass
            
            cur.execute('INSERT INTO oldposts VALUES(?)', [cid])
            sql.commit()
        
while True:
    login(r)
    replyBot(r)
    print('Waiting ' + str(WAIT) + ' seconds')
    time.sleep(WAIT)
