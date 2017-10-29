import httplib, urllib, base64, json, requests
from data_scrape import get_playlist

def grabPlaylist(auth_key):

    headers = {
        # Request headers. Replace the placeholder key below with your subscription key.
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '3a93c7dd2b134f96aa0be44a7af92dda',
    }

    params = urllib.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    body = "{ 'url': 'https://s3.us-east-2.amazonaws.com/azureemotion992/face.jpg' }"

    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the
        #   URL below with "westcentralus".
        conn = httplib.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        d = json.loads(data)
        strongest = 'sadness'
        strongest_val = d[0]['scores']['sadness']
        for emotion in d[0]['scores']:
            if d[0]['scores'][emotion] > strongest_val:
                strongest_val = d[0]['scores'][emotion]
                strongest = emotion

        emotion_map = {'sadness':1, 'anger':2, 'contempt':0, 'disgust':0, 'fear':3, 'happiness':0, 'neutral':3, 'sadness':1, 'surprise':2}

        playlist_uri = get_playlist(emotion_map[strongest], auth_key)

        headers = {"Authorization" : "Bearer "+refresh()}
        body = {'context_uri' : playlist_uri}
        request = requests.put('https://api.spotify.com/v1/me/player/play', headers=headers, body=body)

        conn.close()
    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))
