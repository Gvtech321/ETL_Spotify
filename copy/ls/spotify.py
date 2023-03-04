import json

import spotipy
import requests
from spotipy.oauth2 import SpotifyClientCredentials

#https://stmorse.github.io/journal/spotify-api.html

#to extract names of albums released by artist

def get_albums_artist(albumType,uriName):

    spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

    results = spotify.artist_albums(uriName, albumType)
    albums = results['items']
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])

    for album in albums:
        print(album['name'])

# get credentials
def get_credentials(filePath='pass.txt'):
    with open(filePath,'r') as f:
        return json.load(f)

def connect_spotify():
    credentials=get_credentials()
    clientId=credentials['spotify']['clientId']
    clientSecret=credentials['spotify']['secret_token']
    authUrl=credentials['spotify']['authUrl']
    baseUrl=credentials['spotify']['baseUrl']
    auth_response = requests.post(authUrl, {
        'grant_type': 'client_credentials',
        'client_id': clientId,
        'client_secret': clientSecret,
    })
    auth_response_data=auth_response.json()
    access_token=auth_response_data['access_token']
    return access_token,baseUrl

def get_artist_albums(token,artistId,baseUrl):
    headers = {
        'Authorization': 'Bearer {token}'.format(token=access_token)
    }
    r = requests.get(baseUrl + 'artists/' + artistId + '/albums',
                     headers=headers,
                     params={'include_groups': 'album', 'limit': 50})
    data=r.json()
    return data

access_token,baseUrl=connect_spotify()
artistId='36QJpDe2go2KgaRleHCDTp'
data=get_artist_albums(access_token,artistId,baseUrl)
print(data)




