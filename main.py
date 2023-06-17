from bs4 import BeautifulSoup
import requests

# Scraping Billboard 100 top songs for a particular date
print("Welcome to the Music Time Machine!")
date= input("Where do you want to travel? Type the date in this format YYYY-MM-DD: \n")
url= f"https://www.billboard.com/charts/hot-100/{date}/"
response= requests.get(url)
webpage= response.text


soup= BeautifulSoup(webpage,"html.parser")

titles= [item.getText().strip() for item in soup.select(selector="li ul li h3")]
artists = [item.getText().strip() for item in soup.select(selector="li ul li span") if item.getText().strip()]
artists = [artist for artist in artists if any(char.isalpha() for char in artist)]
title_and_artist = dict(zip(titles, artists))
title_and_artist= [(title, artist) for title, artist in title_and_artist.items()]

print(titles)
print(len(titles))
print(artists)
print(len(artists))
print(title_and_artist)
print(len(title_and_artist))



# Spotify Authentication
#You need to search for your client id and secret id by registering your account into the developers dashboard
import spotipy
from spotipy.oauth2 import SpotifyOAuth
sp = spotipy.Spotify(
auth_manager=SpotifyOAuth(
scope="playlist-modify-private",
redirect_uri="https://example.com/", # this is used only because required, only need a valid random address
client_id="YOURCLIENTID", #Here you will need your own credentials
client_secret="YOURCLIENTESECRETID", #Here you will need your own credentials
show_dialog=True,
cache_path="token.txt" # this will save the temporal token in this path
)
)
user_id = sp.current_user()["id"] #output: your user_id visible in spotify, you could put it as input instead

#Search for Billboard songs in Spotify

song_uris = [] #we will get from spotify the uris searching by song name and artist name
for song in title_and_artist:
    try:
        result = sp.search(q=f"track:{song[0]} artist: {song[1]}", type="track")
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except:
        pass

print(f"Number of songs found: {len(song_uris)}") #To check if all 100 songs were found

#Create the private playluist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)

#Add the scraped billboards songs to this playlist through the URIs
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)

#DONE!