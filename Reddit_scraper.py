from urllib.request import urlopen
import datetime
import requests
import requests.auth
# import praw
import re

class RedditScraper:
    def __init__(self, client_id = None, client_secret = None, username = None, password = None):
        """
        Initialize a client authorization of a Reddit web scraping bot.
        Make sure to use Reddit account with no 2FA! Otherwise OAuth will fail.
        Check out this page for more details https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example
        """
        client_id = client_id
        if client_id is None:
            client_id = input("Enter your Reddit bot approved client_id (if confused read HELPME): ")
        client_secret = client_secret
        if client_secret is None:
            client_secret = input("Enter your Reddit bot approved client_secret (if confused read HELPME): ")
        username = username
        if username is None:
            username = input("Enter your Reddit bot approved username (if confused read HELPME): ")
        password = password
        if password is None:
            password = input("Enter your Reddit bot approved password (if confused read HELPME): ")
        self.client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
        self.post_data = {"grant_type": "password", "username": username, "password": password}
        self.headers = {"User-Agent": f"MyAPI/0.1 by {username}"}
        self.response = requests.post("https://www.reddit.com/api/v1/access_token", auth=self.client_auth, data=self.post_data, headers=self.headers)
        self.TOKEN = self.response.json()['access_token']
        self.headers['Authorization'] = f'bearer {self.TOKEN}'

    def get_page(self, page):
        """
        This method bypasses Reddit API.
        """
        urlopenhtml = urlopen(f"https://old.reddit.com{page}")
        html = urlopenhtml.read().decode('utf-8')
        return html

    def get_active_user_json(self, page):
        """
        Must be "/r/{subreddit_name_here}" format
        """
        page = requests.get(f"https://oauth.reddit.com{page}/about", headers = self.headers).json()
        if page["data"]: # if page.json has a data key
            if page["data"]["active_user_count"]: # if page.json has a data key AND an active user count key
                active_user = page["data"]["active_user_count"]
                if page["data"]["display_name"]:  # if page.json has a data key AND an active user count key
                    subreddit_name = "/r/" + page["data"]["display_name"]
                else:
                    subreddit_name = page
            else:
                active_user = None
        else:
            active_user = None
            subreddit_name = page
        return active_user, datetime.datetime.now(), subreddit_name

    def get_active_user(self, page):
        """
        Must be "/r/{subreddit_name_here}/" format
        """
        html = self.get_page(page)
        x = re.findall('<p class="users-online".*?[^/]</span>', html)
        active_number = re.findall(r'\d+', str(x))
        active_number = active_number[1:] # Remove the first 15 in the parsed string
        active_user = ""
        for s in active_number:
            active_user += s
        active_user = int(active_user)
        return active_user, datetime.datetime.now()

## BeautifulSoup HTML parsing method...
# from bs4 import BeautifulSoup
# html_2 = urlopen("https://old.reddit.com/r/orangetheory").read().decode('utf-8')
# soup = BeautifulSoup(html_2, "html.parser")
# number = soup.find_all("span", class_="number")
# for tag in number:
#     print(tag)