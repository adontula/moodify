from sklearn.ensemble import RandomForestClassifier
import pandas as pd
import numpy as np
import json
import requests
from sklearn.metrics import mean_absolute_error as mae
from sklearn.model_selection import train_test_split as tts

model = RandomForestClassifier(n_jobs=-1, random_state=0)

def run_model():
    global model
    reactions = open('reactions.data', 'r').read()
    reacts = []
    for reaction in reactions:
        try:
            reacts.append(int(reaction.replace(' ', '').replace('\n', '')))
        except:
            pass

    print(len(reacts))

    x = pd.read_json('songs.data')
    print(x.describe())

    x['result'] = reacts
    x = x[x.result != 5]

    x['is_train'] = np.random.uniform(0, 1, len(x)) <= .75
    train, test = x[x['is_train']==True], x[x['is_train']==False]

    drops = ['result', 'id', 'name']

    Y_train = train.result
    X_train = train.drop(drops, axis=1)

    print(X_train.describe())

    Y_val = test.result
    X_val = test.drop(drops, axis=1)

    model.fit(X_train, Y_train)
    predictions = model.predict(X_val)
    print(X_val)

    c = 0
    for num in range(len(X_val)):
        if predictions[num] != Y_val.iloc[num]:
            print(x.loc[num, 'id'])
        else:
            c += 1
    print(predictions)
    print('ACCURACY: ' + '{:.3f}'.format(float(c)/len(predictions) * 100) + "%")

def calculate_mood():
    #client = MongoClient("mongodb://admin:hacktx2017@cluster0-shard-00-00-rpkjr.mongodb.net:27017,cluster0-shard-00-01-rpkjr.mongodb.net:27017,cluster0-shard-00-02-rpkjr.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin")
    #db = client.test

    global model
    x = pd.read_json('songs.data')
    x['is_train'] = False
    print(x.describe())

    drops = ['id', 'name']

    X_val = x.drop(drops, axis=1)

    print(X_val)
    predictions = model.predict(X_val)

    #posts = db.posts
    post_data = []

    for num in range(len(predictions)):
        post_data.append({
            'id':x['id'][num],
            'emotion':str(predictions[num])
        })
    #posts.insert_many(post_data)
    headers = {"Content-Type" : "application/json"}
    request = requests.post("https://api.mlab.com/api/1/databases/emotion_music/collections/prediction_data?apiKey=7fjUwhTEJe2ALljJOyn706HsWtIJxvvB", headers=headers, data=json.dumps(post_data))
