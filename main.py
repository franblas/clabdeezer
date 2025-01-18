import time
import json
import sqlite3
import requests
from bs4 import BeautifulSoup


def fetch_clab_data():
    rep = requests.get("https://www.c-lab.fr/grille/quel-est-ce-titre")
    return rep.text


def parse_track(track):
    artist_ = track.find("div", {"class": "track-history__item__artist"}).text.strip()
    time_ = track.find("div", {"class": "track-history__item__time"}).text.strip()
    title_ = track.find("div", {"class": "track-history__item__titre"}).text.strip()
    raw_spotify_id_ = track.find("a", {"class": "track-history__item__spotify"})
    if not raw_spotify_id_:
        return {"time": None, "title": None, "artist": None, "spotify_id": None}
    spotify_id_ = raw_spotify_id_.attrs["href"].strip().replace("spotify:track:", "")
    return {"time": time_, "title": title_, "artist": artist_, "spotify_id": spotify_id_}


def get_tracks(raw_data):
    soup = BeautifulSoup(raw_data, "html.parser")
    tracks = soup.find_all("div", {"class": "track-history__item"})
    return [parse_track(track) for track in tracks]


def fetch_deezer_data(title, artist):
    rep = requests.get('https://api.deezer.com/search?q=artist:"' + artist + '" track:"' + title + '"')
    return rep.json()


def main():
    conn = sqlite3.connect("clabdeezer.db")
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tracks
    (id text primary key, title text, artist text, deezer text, intoplaylist integer)
    ''')
    rawdata = fetch_clab_data()
    track_list = get_tracks(rawdata)
    for t in track_list:
        print(t)
        idd = t["spotify_id"]
        if not idd:
            continue
        ddata = fetch_deezer_data(t["title"], t["artist"])
        cursor.execute('''
        INSERT OR IGNORE INTO tracks (id, title, artist, deezer, intoplaylist) VALUES (?, ?, ?, ?, ?)
        ''', (idd, t["title"], t["artist"], json.dumps(ddata), None))
        conn.commit()
        time.sleep(3)
    conn.close()


if __name__ == '__main__':
    main()
