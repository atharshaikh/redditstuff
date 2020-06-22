import psycopg2
from config import dbinit, reddinit
import praw
import datetime

t = datetime.datetime.now()
t_final = int(datetime.datetime(year=t.year, month=t.month, day=1).timestamp())

reddit = praw.Reddit(**reddinit())
subs = []
for i in reddit.redditor("youruserhere").moderated():
    subs.append(i.display_name)
conn = psycopg2.connect(**dbinit())
cur = con.cursor()

sql_insert = "INSERT INTO {} VALUES ('{}','{}','{}',{},'{}','{}');"
sql_create = 'CREATE TABLE IF NOT EXISTS {} ("mod" TEXT,"action" TEXT,"target_author" TEXT,"created_utc" INTEGER,"id" TEXT UNIQUE,"target_permalink" TEXT);'
sql_get_time = "SELECT MAX(created_utc) from {};"
for i in subs:
    print(i)
    sb = reddit.subreddit(i)
    cur.execute(sql_create.format(i))
    cur.execute(sql_get_time.format(i))
    time = cur.fetchone()[0]
    count = 0
    if time is None:
        time = t_final
    for j in sb.mod.log(limit=None):
        if j.created_utc < time:
            break
        try:
            cur.execute(
                sql_insert.format(
                    i,
                    j.mod,
                    j.action,
                    j.target_author,
                    j.created_utc,
                    j.id,
                    j.target_permalink,
                )
            )
            con.commit()
        except psycopg2.errors.UniqueViolation:
            print(j.id)
            con.rollback()
        except Exception as e:
            print(e, j.id)
            con.rollback()
        count += 1
        if count % 500 == 0:
            print(count)
    con.commit()
    print(f"Total actions since last update: {count}")
    print(f"{i} is done")
con.commit()
con.close()
