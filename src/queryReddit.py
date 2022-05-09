import praw
import pandas as pd
from datetime import datetime
import pymongo



mongo_credentials = ""

client = pymongo.MongoClient(mongo_credentials)
db = client['reddit']
collection = db['philosophy']

posts = []
hot_posts = reddit.subreddit('philosophy').top(limit=1000)
print('fin')
for post in hot_posts:
    print(' ')
    parsed_date = datetime.utcfromtimestamp(post.created)
    year = parsed_date.year
    month = parsed_date.month
    day = parsed_date.day
    date = str(day)+'/'+str(month)+'/'+str(year)
    posts.append([post.title, post.score, post.id, post.url, date])

posts = pd.DataFrame(posts,columns=['title', 'score', 'id',  'url', 'created'])
print(posts)

def convertToCSVfile(df):
    df.dropna()
    df.drop_duplicates(keep='first')
    print(df)
    df.to_csv('redditData.csv', encoding='utf-8', index=False)
def pushToMongo(df):
    # Our mongo cluster can store 52 million tweets
    collection.insert_many(df.to_dict('records'))

pushToMongo(posts)

convertToCSVfile(posts)    

