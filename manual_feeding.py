import sqlite3
import json
import webbrowser

browser = webbrowser.get('firefox')
conn = sqlite3.connect("clabdeezer.db")
cursor = conn.execute('''SELECT * FROM tracks WHERE intoplaylist is NULL ORDER BY id DESC''')
reps = cursor.fetchall()
print("Remaining songs to add", len(reps))
for row in reps:
    deezer_data = json.loads(row[3])["data"]
    if len(deezer_data) > 0:
        idd = row[0]
        print("idd", idd)
        link = deezer_data[0]["link"]
        print("link", link)
        browser.open(link)
        input("Press Enter to continue...")
        conn.execute('''UPDATE tracks SET intoplaylist = ? WHERE id = ?''', (1, idd))
        conn.commit()
conn.close()