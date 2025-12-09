import os
import json
import time
import random
import sqlite3
from urllib.parse import quote #need this to not mess up the url otherwise the API calls don't work properly 
from api_tls_client_setup import TrackerAPI  

#whole point is to use tls to scrape match data from tracker.gg without obviously being idetnified as a bot
#otherwise i get my cookie banned (already happened once) and i have to wait a long time to try again 
#need to have random points where I have wait timers otherwise its obvious 
#whenever cloudfare rate limits, need to wait a much longer time to avoid multiple rate limits in a row and getting banned
#

#databse setup using sqlite3 syntax
def init_db():
    conn = sqlite3.connect("full_matches.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS full_matches (
            match_id TEXT PRIMARY KEY,
            raw_json TEXT
        )
    """)
    conn.commit()
    conn.close()


#insert full match data into database table 
def insert_full_match(match_id, raw_json):
    conn = sqlite3.connect("full_matches.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT OR REPLACE INTO full_matches (match_id, raw_json)
        VALUES (?, ?)
    """, (match_id, raw_json))
    conn.commit()
    conn.close()




def main():
    #initialize the database 
    init_db()
    #read match id master list file, all of them are one match id on each line w/o spaces 
    with open("match_id_master_list.txt", "r", encoding="utf-8") as match_id_file:
        match_ids = match_id_file.read().splitlines()

    #make the api object using the other python script 
    api = TrackerAPI()

    for idx, match_id in enumerate(match_ids):
        match_ids[idx] = match_id.strip()

        tracker_gg_match_id = quote(match_id, safe="")
        url = f"https://api.tracker.gg/api/v2/marvel-rivals/standard/matches/{tracker_gg_match_id}"

        # Try to get match data w/ api call and insert into database
        try:
            data = api.get(url)
            insert_full_match(match_id, json.dumps(data))
        except Exception as e:
            print(f"error: {e}")
            #slep 
            time.sleep(random.uniform(5.1, 10.7))
            continue

        #more random delays here bc cloudfare keeps rate limitting me 
        time.sleep(random.uniform(5.1, 10.7))
        #do another wait time after every 25 matches grabbed to make it less obvious
        if (idx + 1) % 25 == 0:
            pause = random.uniform(60, 120)
            print(f"pausing at {idx +1}")
            time.sleep(pause)

if __name__ == "__main__":
    main()
