import sys
import requests
import json
from model import calculate_mood

def readTracks(auth_key):

    fi = open("songs.data", "a")
    # fi2 = open("nameIdRelation.txt", "a")

    # initial setup, currently using hard-coded authorization
    payload = {"limit" : 50, "offset" : 0}
    headers = {"Accept" : "application/json", "Authorization" : "Bearer "+auth_key}
    track_request = requests.get("https://api.spotify.com/v1/me/tracks", params=payload, headers=headers)
    data = track_request.json()
    total = data["total"]

    # run the analysis until reaching the end of the list
    data_array = []
    while total > 0:
        total -= 50
        for item in data["items"]:
            id = (item["track"]["id"])

            query_headers = {"Content-Type" : "application/json"}
            query_request = requests.get("https://api.mlab.com/api/1/databases/emotion_music/collections/prediction_data?apiKey=7fjUwhTEJe2ALljJOyn706HsWtIJxvvB&q={\"id\":\""+id+"\"}", headers=query_headers)
            if len(json.loads(query_request.text)) == 0:
                name = item["track"]["name"]
                url = "https://api.spotify.com/v1/audio-features/"
                url = url + id
                feature_request = requests.get(url, headers=headers)
                feature = feature_request.json()
                data = {
                    "id" : feature["id"],
                    "energy" : feature["energy"],
                    "loudness" : feature["loudness"],
                    "mode" : feature["mode"],
                    "speechiness" : feature["speechiness"],
                    "tempo" : feature["tempo"],
                    "valence" : feature["valence"],
                    "name" : item["track"]["name"]
                }
                data_array.append(data)
                # fi2.write("id: {} | name: {}\n".format( feature["id"] ,name))
                # print data
                # dict_data.append(data)
        if total > 0 :
            payload["offset"] += 50


        track_request = requests.get("https://api.spotify.com/v1/me/tracks", params=payload, headers=headers)
        data = track_request.json()


    fi.write(str(json.dumps(data_array)))

    calculate_mood()

def readPlayList():

    f2 = open("playlist_songs.data", "a")
    fi2 = open("nameIdRelation.data", "a")
    url = "https://api.spotify.com/v1/users/" + "lockijazz" +"/playlists/"  + "0KxCwQWV2dag4n81XQNu2K" + "/tracks"
    headers = {"Accept" : "application/json", "Authorization" : "Bearer " + auth_key}
    payload = {"limit" : 50}
    playlist_request = requests.get(url, headers = headers, params=payload)
    data = playlist_request.json()
    f2.write("[")
    for item in data["items"]:
        url = "https://api.spotify.com/v1/audio-features/"
        url = url + item["track"]["id"]
        feature_request = requests.get(url, headers=headers)
        feature = feature_request.json()
        song = {
            "id" : feature["id"],
            "energy" : feature["energy"],
            "loudness" : feature["loudness"],
            "mode" : feature["mode"],
            "speechiness" : feature["speechiness"],
            "tempo" : feature["tempo"],
            "valence" : feature["valence"],
            "name" : item["track"]["name"]
        }
        f2.write(str(song) + ",")
        fi2.write("id: {} | name: {}\n".format( feature["id"] , item["track"]["name"]))
    f2.write("]")



def get_playlist(emotion, auth_key):

    # initial setup, currently using hard-coded authorization
    payload = {"limit" : 50, "offset" : 0}
    headers = {"Accept" : "application/json", "Authorization" : "Bearer " + auth_key}
    track_request = requests.get("https://api.spotify.com/v1/me/tracks", params=payload, headers=headers)
    data = track_request.json()
    total = data["total"]
    dict_data = []

    emotions = ["Happy", "Sad", "Hyped", "Calm"]

    user_id = "GOOSH" # change to get it from amans app as well as all the authorization codes
    playlist_headers = {"Content_Type" : "application/json", "Authorization" : "Bearer " + auth_key}
    playlist_body = json.dumps({"name":emotions[emotion], "description":"Playlist Built By: HackTX 2017 Emotion-Spotify Playlist Generator"})
    playlist_create_request = requests.post("https://api.spotify.com/v1/users/"+user_id+"/playlists", headers=playlist_headers, body=playlist_body)
    playlist_uri = playlist_create_request.json()["uri"]

    data_uris = []

    # run the analysis until reaching the end of the list
    while total > 0:
        total -= 50
        for item in data["items"]:
            id = (item["track"]["id"])

            query_headers = {"Content-Type" : "application/json"}
            query_request = requests.get("https://api.mlab.com/api/1/databases/emotion_music/collections/prediction_data?apiKey=7fjUwhTEJe2ALljJOyn706HsWtIJxvvB&q={\"id\":\""+id+"\", \"emotion\":"+emotion+"}", headers=query_headers)
            if len(json.loads(query_request.text)) > 0:
                data_uris.append(item["track"]["uri"])


        if total > 0 :
            payload["offset"] += 50

        track_request = requests.get("https://api.spotify.com/v1/me/tracks", params=payload, headers=headers)
        data = track_request.json()

    playlist_add_body = json.dumps({"uris": str(data_uris)})
    playlist_add_request = requests.post("https://api.spotify.com/v1/users/"+user_id+"/playlists/"+playlist_id+"/tracks", headers=playlist_headers, body=playlist_add_body)

    return playlist_uri



    # input
    # energy, loudness, mode, speechiness, tempo, valence
