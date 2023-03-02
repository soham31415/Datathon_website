import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(from:UTDTrey) until:2023-03-01 since:2023-02-26 -filter:replies"
tweets = []
limit = 10

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.user.username, tweet.content])
    
df = pd.DataFrame(tweets, columns=['User', 'Tweet'])

print(df)