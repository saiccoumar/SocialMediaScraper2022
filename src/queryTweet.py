# Bearer Token


import requests
import json
import pandas as pd
from pandas import json_normalize
import pymongo 


bearer_token =  'bearer_token'
mongo_credentials = "mongo_credentials"

client = pymongo.MongoClient(mongo_credentials)
db = client['twitter']
collection = db['philosophy']
print(client.list_database_names())
headers = {"Authorization": "Bearer "+bearer_token}

# Work on filtering retweets

def search_twitter(query, max_results):
    tweet_fields = "tweet.fields=author_id,text,created_at,geo"
    url = "https://api.twitter.com/2/tweets/search/recent?query=" + query + "&" + tweet_fields + "&max_results="+ str(max_results) 


    if ((max_results < 10) or (max_results>100)):
        url = "https://api.twitter.com/2/tweets/search/recent?query="  + query  + "&" + tweet_fields 
    response = requests.request("GET", url, headers=headers)

    print(response.status_code)

    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()
    
def convertToCSVfile(jsonObj):
    df = json_normalize(jsonObj)
    df.dropna()
    df.drop_duplicates(keep='first')
    print(df)
    df.to_csv('test.csv', encoding='utf-8', index=False)

#pretty printing
def printData(jsonObj):
    count = 0
    for i in jsonObj:
        count += 1
        print(i['text'])
        # print(i)
        print("New Tweet:")
    print("Length: "+str(count))


def pushToMongo(jsonObj):
    # Our mongo cluster can store 52 million tweets
    for i in jsonObj:
        collection.insert_one(i)

#search term
query = "philosophy"


#twitter api call
count = 0 
while count<10000:
    count += 1
    json_response = search_twitter(query,100)
    convertToCSVfile(json_response['data'])
    printData(jsonObj=json_response['data'])
    pushToMongo(jsonObj=json_response['data'])


# collected = list(collection.find({}))
# # print("total docs in collection:", collection.count_documents( {} ))
# # print ("total docs returned by find():", len(list(collected)))
# collectionDf = pd.DataFrame(collected)
# collectionDf = collectionDf.drop(columns=['_id','geo'])
# collectionDf = collectionDf.drop_duplicates(subset=['id'],keep='first')
# print(collectionDf)
# collectionDf.to_csv('data.csv', encoding='utf-8', index=False)

# TEST
# json_response = search_twitter(query,10)
# print(json_response)
# convertToCSVfile(json_response['data'])
# printData(jsonObj=json_response['data'])