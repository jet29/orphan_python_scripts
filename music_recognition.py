import requests
import glob
import ntpath
from pydub import AudioSegment
import json
import mutagen
from mutagen.mp3 import MP3
from mutagen.id3 import ID3
from mutagen.easyid3 import EasyID3
import os

# THINGS TO FIX: DUPLICATED SONGS CANT BE WRITEN


def TimeMilis(seconds, minutes = 0, hours = 0):
    return hours*60*1000 + minutes*60*1000 + seconds*1000


def MakeRequest(binaryFile):
    print("making request...")

    data = {
        'api_token': 'test'
    }

    files = {
        'file': binaryFile,
    }

    return requests.post('https://api.audd.io/', data=data, files=files).text

def ChangeSongMetadata(parsedJson, fileName):
    print("changing song metadata")
    
    try:
        audio = EasyID3(fileName)

    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(fileName, easy=True)
        audio.add_tags()
    
    audio["title"] = parsedJson["result"]["title"]
    audio["artist"] = parsedJson["result"]["artist"]
    audio["album"] = parsedJson["result"]["album"]
    audio["originaldate"] = parsedJson["result"]["release_date"]

    audio.save()

    artist = parsedJson["result"]["artist"].upper()
    name = parsedJson["result"]["title"].upper()

    illegal = ['\\','/',':','*','"','<','>','|','?']
    
    for i in illegal:
        artist = artist.replace(i, '')
        name = name.replace(i, '')

    newName =  artist + " - " + name + ".mp3"
    os.rename(fileName,newName)


def main():
    allSongs = glob.glob("./*.mp3")

    for song in allSongs:

        fileName = ntpath.basename(song)
        print("changing song: " + fileName)

        # Get a part of the song
        startMin = 0
        startSec = 20
        endMin = 0
        endSec = 40

        # Time to miliseconds
        startTime = TimeMilis(startSec,startMin)
        endTime = TimeMilis(endSec,endMin)

        # Opening file and extracting segment
        songSegment = AudioSegment.from_mp3( song )
        extract = songSegment[startTime:endTime]

        # Saving
        extract.export('song-extract.mp3', format="mp3")

        # Make Request
        fileRead = open('./song-extract.mp3', 'rb')
        result = MakeRequest(fileRead) # return json text
        print(result)
        fileRead.close()

        parsedJson = json.loads(result)

        if parsedJson["status"] == "success" and parsedJson["result"] != None: 
            ChangeSongMetadata(parsedJson, fileName)
        else:
            print("failed to get song information")

        os.remove("./song-extract.mp3")


if __name__ == "__main__":
    main()



