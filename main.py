import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "" #your cllient id
SPOTIPY_CLIENT_SECRET = "" #your client secret
SPOTIPY_REDIRECT_URI = "http://example.com"


date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)
billboard_web_page = response.text

soup = BeautifulSoup(billboard_web_page, "html.parser")
song_names_spans = soup.find_all("h3", class_="a-no-trucate")
song_names = [song.getText().strip("\n\n\t\n\t\n\t\t\n\t\t\t\t\t") for song in song_names_spans]

# for song in songs_name:
#     title = song.getText()
#     songs_name.append(title)

# print(songs_list)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=SPOTIPY_REDIRECT_URI,
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"] # the output of this method is a dic, we look for the value of the "id" key.
print(user_id)

song_uris = []

year = date.split("-")[0]

for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100.", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
