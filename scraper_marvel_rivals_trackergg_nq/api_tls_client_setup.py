import tls_client
import time
import random


USER_AGENT = "Browswer user agent from chrome dev tools: ex: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
COOKIE = "I had to delete my cookie for privacy purposes"
#initializing tls client stuff
class TrackerAPI:
    def __init__(self):
        self.client = tls_client.Session(
            client_identifier="chrome_142",
            random_tls_extension_order=True
        )

        #headers common to all requests
        self.headers = {
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://tracker.gg/",
            "Origin": "https://tracker.gg",
            "Sec-Fetch-Site": "same-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Cookie": COOKIE,
        }

    def get(self, url):
        for i in range(0, 2): #i only want to try 2x max otherwise move on
            #random sleep event in between requests 
            time.sleep(random.uniform(1.1, 3.2)) #range so that it looks more human less bot like

            try:
                response = self.client.get(url, headers=self.headers)
                status = response.status_code
                #if rate limitted, wait and retry again after some time, but try random wait time
                if status == 429:
                    #whenever cloudfare rate limits, need to wait a much longer time to 
                    #avoid multiple rate limits in a row and getting banned
                    wait_time = random.uniform(303, 908) #random wait between 5-15 min, but not exactly so its obvious
                    print('rate limited, sleeping')
                    time.sleep(wait_time)
                    continue
                #if success response = 200, grab json data
                if status == 200: 
                    return response.json()

            except Exception as e:
                print(f"error: {e}")
        
        return None
