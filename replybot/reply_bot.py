import praw
import sqlite3
import time
import re
import os

t1 = time.perf_counter()

# get absolute filepath and db path
# system independent
filepath = os.path.dirname(os.path.abspath(__file__))
db = os.path.join(filepath, "data.db")

# initialise db connection and cursor objects
con = sqlite3.connect(db)
cur = con.cursor()

# get login details from db
cur.execute("SELECT * FROM login_data")
data = [i for i in cur.fetchone()]
# print(data)

# initialise reddit instance
reddit = praw.Reddit(
    client_id=data[0],
    client_secret=data[1],
    user_agent=data[2],
    username=data[3],
    password=data[4],
)


# reply to comment/submission, depending upon value passed to it
def reply(case, robj):
    # get pointer to random string, and then string
    get_random_cursor = cur.execute(
        f"SELECT {case} FROM REPLY ORDER BY RANDOM() LIMIT 1"
    )
    random_string = get_random_cursor.fetchone()[0]
    # reply to object
    x = robj.reply(random_string)
    # sleep, else distinguish doesnt work
    time.sleep(2)
    x.mod.distinguish(how="yes")
    # insert post/submission id into db
    # so as to prevent further replies
    cur.execute("INSERT INTO replied_to VALUES(?)", (robj.id,))
    con.commit()


# check for matching syntax
def case1(text, selftext=None):
    check_phrase = ["word1", "word2"]
    pattern = re.compile("|".join(check_phrase), re.IGNORECASE)
    # works with both, comments and posts, as called with respective functions
    # if selftext doesn't exist, submission.selftext is none
    if selftext:
        return re.search(pattern, text) or re.search(pattern, selftext)
    else:
        return re.search(pattern, text)


def main():
    c = 0
    last_comment, last_post = None, None

    # exclude bots, and maybe users
    exclude_users = ["botusername", "automoderator", "totesmessenger", "none"]
    # initialise subreddit instance
    subreddit = reddit.subreddit("librandu")

    # going through last 100 comments
    for comment in subreddit.comments():
        # get newest
        if c == 0:
            last_comment = comment.id
            c += 1
        # do nothing if author is either of [deleted] or [removed]
        if comment.author is None:
            continue
        name = comment.author.name
        # do nothing if author is a bot or
        # someone who's requested to not be replied to
        if name.lower() in exclude_users:
            continue
        # check if the current comment has already been replied to.
        # if yes, then you can break
        cur.execute(
            "SELECT permalink FROM replied_to WHERE permalink = ?", (comment.id,)
        )
        if cur.fetchall():
            break
        # check if it satisfies the condition
        if case1(comment.body):
            # if yes, then reply and add value to db
            reply("case1", comment)

    # go through newest 100 submissions
    for submission in subreddit.new():
        # get newest submission
        if c == 1:
            last_post = submission.id
            c += 1
        # do nothing if author doesn't exist
        if submission.author is None:
            continue
        name = submission.author.name
        # do nothing if author is a bot or
        # someone who's requested to not be replied to
        if name.lower() in exclude_users:
            continue
        # check if the current submission has already been replied to.
        # if yes, then you can break
        cur.execute(
            "SELECT permalink FROM replied_to WHERE permalink = ?", (submission.id,)
        )
        if cur.fetchall():
            break
        # check if it satisfies the condition
        if case1(submission.title, submission.selftext):
            # if yes, then reply and add value to db
            reply("case1", submission)

    meta = (time.strftime("%d.%m.%Y %H:%M %z"), last_comment, last_post)
    cur.execute("INSERT INTO metadata VALUES (?, ?, ?)", meta)
    con.commit()


try:
    main()
except Exception as e:
    print(e)

tm = os.path.join(filepath, "time.txt")
with open(tm, mode="a", encoding="utf-8") as s:
    s.write(f"{time.perf_counter() - t1:.2f} \n")
