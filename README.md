# Clab To Deezer
Scripts to fetch songs played on clab radio and push them on a deezer playlist (auto or manually)

## Requirements
- Python 3.11+
- Pip 21+
- Install deps
```
pip install -r requirements.txt
```

## Fetch songs
Just run
```
python main.py
```

All songs are stored into sqlite `clabdeezer.db`

| id      | title      | artist      | deezer      | intoplaylist      |
| ------------- | ------------- | ------------- | ------------- | ------------- |
| unique id of the song | song name | artist name | associated deezer data | flag used for manual feeding |

## Feeding
### Auto
Not possible currently, Deezer has temporarily shutdown some components of the API included private playlist feeding. 

### Manual
Open Firefox browser, then connect to deezer account through main website.
Then run
```
python manual_feeding.py
```
Once you are done with a song press enter on python side to open the next track

Nb: if you want to use another webbrowser, change the line 5 of the script and set your favorite browser
```
browser = webbrowser.get('mayfavoritebrowser')
```
Available browser list : [https://docs.python.org/3/library/webbrowser.html](https://docs.python.org/3/library/webbrowser.html)
