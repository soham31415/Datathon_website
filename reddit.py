import praw

def redScrape():
    user_agent = "Scraper 1.0"
    reddit = praw.Reddit(
        client_id = "CCR9qratPsoFxW6lUtLsiA",
        client_secret = "DrlkhN7yc9u0tgj1caxThBcNzjB-sA",
        user_agent=user_agent
    )

    headlines = set()
    for submission in reddit.subreddit('politics').hot(limit=1):
        print(submission.author)
        print(submission.title)
        print(submission.selftext)

redScrape()