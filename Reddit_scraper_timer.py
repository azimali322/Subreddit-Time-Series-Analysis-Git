from Reddit_scraper import RedditScraper
import time, datetime
import os.path
import random
import csv
import pandas as pd

class Reddit_scraper_timer:
    def __init__(self, c_id, c_secret, uname, pword, list_of_subreddits_to_poll):
        self.c_id = c_id
        self.c_secret = c_secret
        self.uname = uname
        self.pword = pword
        self.list_of_subreddits_to_poll = list_of_subreddits_to_poll

    def auto_timer(self, parsing_interval = 900, seconds_delay = 0, minutes_delay = 0, hours_delay = 0, days_delay = 0, weeks_delay = 0):
        header = ["DateTime", "Subreddit", "Active_Users"]
        data = []
        # Initialize data list if file already exists.
        if os.path.exists('SubredditActiveUsersParsed.csv'):
            existing_csv = pd.read_csv('SubredditActiveUsersParsed.csv', header=0)
            data = existing_csv.values.tolist()
        cur_date = datetime.datetime.now()
        delta_days = datetime.timedelta(seconds= seconds_delay, minutes = minutes_delay, hours= hours_delay, days= days_delay, weeks= weeks_delay) # How long will this program run?
        stop_date = cur_date + delta_days
        rs = RedditScraper(self.c_id, self.c_secret, self.uname, self.pword)
        while datetime.datetime.now() < stop_date:
            for subreddit in self.list_of_subreddits_to_poll:
                try:
                    res = rs.get_active_user_json(subreddit)
                except:
                    res = None, datetime.datetime.now(), subreddit
                data_res = []
                data_res.append(res[1])
                # data_res.append(subreddit)
                data_res.append(res[2])
                data_res.append(res[0])
                print(res[1], res[2], res[0])
                data.append(data_res)
            lower_delay = random.uniform(0, 0.5)
            upper_delay = random.uniform(0, 0.5)
            delay_secs = random.uniform(parsing_interval - lower_delay, parsing_interval + upper_delay)
            with open('SubredditActiveUsersParsed.csv', 'w', encoding='UTF8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(header)
                writer.writerows(data)
            time.sleep(delay_secs)
        print("Done.")