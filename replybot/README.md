## Basic Auto-Reply bot, made for /r/Librandu

# How to use

1) Ensure Python 3.4+ and PRAW are installed on your system. `pip install praw`
2) Register your script on reddit. Follow the instructions available on the the PRAW documentation site
3) Open "data.db" with a program like DB Browser.
4) Go to Browse Data, in the table *login data* insert your `client_id`, `client_secret`, `user_agent`, `username`, and `password` in the **first row** under their respective columns.
5) Now, go to the table *reply*, and enter the reply strings you need in different rows.
6) Next, open *reply_bot.py*, and in the list `check_phrase` replace the existing words with the words with which you want to trigger the bot, like this:
	`check_phrase = ["word1", "word2", "word3"]`
7) Now run, and.... Profit??
