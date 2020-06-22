import praw
from praw.models import Comment
from config import reddinit

reddit = praw.Reddit(**reddinit())
srd = reddit.subreddit("mod")

count = {}
total = 0
for i in srd.mod.modqueue(limit=None):
    x = i.subreddit.display_name
    if x not in count.keys():
        count[x] = {"Posts": 0, "Comments": 0}
    if isinstance(i, Comment):
        count[x]["Comments"] += 1
        total += 1
    else:
        count[x]["Posts"] += 1
        total += 1

res = sorted(
    count.items(),
    key=lambda itemsort: itemsort[1]["Posts"] + itemsort[1]["Comments"],
    reverse=True,
)

for i in res:
    x, y = i[1].values()
    linbreak = "-" * (len(i[0]) + len(str(x + y)) + 5)
    print(linbreak)
    print(f"|{i[0]} : {x+y}|")
    print(linbreak)
    print("Posts : {} \t Comments : {}".format(x, y))
    print()

print("------------")
print(f"|Total : {total}|")
print("------------")
