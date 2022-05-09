from lib2to3.pytree import convert
import pandas as pd
from facebook_scraper import get_posts
import pymongo

mongo_credentials = "mongo_credentials"

client = pymongo.MongoClient(mongo_credentials)
db = client['Facebook']
collection = db['philosophy']

listgroups = ['groups/Ethpolsocpsy','groups/799987083411428','groups/179082568894625','groups/1574445816100600','groups/SPFH2','groups/760505804439213','groups/philosophyoftruth','groups/EthicsandMoralPhilosophy','groups/241625830221987','groups/physics.philosophy']

listposts = []

for i in listgroups:
    for post in get_posts(i, pages=50):
        # print(post['reactions'])
        print(post['text'])
        print("")
        listposts.append([post['text'], post['post_id'], post['post_url'], post['time']])

posts = pd.DataFrame(listposts,columns=['title', 'id',  'url', 'created'])

def convertToCSVfile(df):
    df.dropna()
    df.drop_duplicates(keep='first')
    print(df)
    df.to_csv('facebookData.csv', encoding='utf-8', index=False)
def pushToMongo(df):
    # Our mongo cluster can store 52 million tweets
    collection.insert_many(df.to_dict('records'))

convertToCSVfile(posts)

pushToMongo(posts)


print(len(listposts))


# def search_facebook(query, max_results):
#     graph = facebook.GraphAPI(access_token=token, version = 2.8)
#     profile = graph.get_object('me',fields='first_name,location,link,email')	
# 	#return desired fields
#     permissions = graph.get_permissions(user_id=131165496141313)
#     return permissions

# print(search_facebook('philosophy',10))