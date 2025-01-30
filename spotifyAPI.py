from openai import OpenAI
from sk import my_sk
from client import client_id
from client import client_secret
from spotipy import Spotify
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import base64
import requests
from PIL import Image

client = OpenAI(
    api_key=my_sk
)

redirect_uri = "http://localhost:5000/callback"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope='playlist-read-private, ugc-image-upload, playlist-modify-private, playlist-modify-public',
    )
)

print("••• Welocome to the spotify cover image generator •••")

while True:
    playlist = input(str("***Enter your playlist name***\n"))
    vibe = input(str("***Enter the vibe of your playlist***\n"))

    response = client.images.generate(
            model="dall-e-3",
            prompt=f"Make an image for my playlist, this is the name of the playlist: {playlist}, here is the vibe of the playlist: {vibe}",
            size="1024x1024",
            quality="standard",
            n=1,
    )

    #Extract the URL of the generated image
    image_url = response.data[0].url
    #HTTP Get request to the specific url
    image_response = requests.get(image_url)

    #Checking the response status code, 200 means successful request
    if image_response.status_code == 200:
        #Opening a file in Write-Binary Mode
        with open("playlist_image.jpg", "wb") as file:
            #Writing the image content to the file
            file.write(image_response.content)
            #Confirmation Message
            print("Image downloaded successfully")
    else:
        #if the response status code is not 200, it prints error message
        print(f"Failed to download image. Status Code: {image_response.status_code}" )

    image = Image.open("playlist_image.jpg")
    image = image.resize((256, 256))
    image.save('playlist_image_256.jpg')


    #Reads the JPEG image into a binary format
    with open("playlist_image_256.jpg", "rb") as image_file:
        #Converts the binary data into a
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")

    id=input("***Input your playlist_id of your spotify playlist to upload your generated cover image***\n")

    sp.playlist_upload_cover_image(id, image_base64)

    Done = input("Would you like to generate another cover image for a playlist (Yes/No)? ").lower()
    if Done == "no":
        False













