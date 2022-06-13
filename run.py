import sys
from Reddit_scraper_timer import Reddit_scraper_timer

def main():
    res = input("Do you have a file in the working directory with Reddit bot details (see README)? (y or n)")
    if res == "y":
        with open('Reddit_bot_info.txt', encoding='utf8') as f:
            idx = 0
            for line in f:
                if idx == 0:
                    c_id = line
                    c_id = c_id[:-1]
                if idx == 1:
                    c_secret = line
                    c_secret = c_secret[:-1]
                if idx == 2:
                    uname = line
                    uname = uname[:-1]
                if idx == 3:
                    pword = line
                idx += 1
    else:
        c_id = input("Enter your Reddit bot approved client_id (if confused read README): ")
        c_secret = input("Enter your Reddit bot approved client_secret (if confused read README): ")
        uname = input("Enter your Reddit bot approved username (if confused read README): ")
        pword = input("Enter your Reddit bot approved password (if confused read README): ")
    stp = input("Do you have certain subreddits that you wish to track? If n, then stick to default tracking subreddits. (y or n)")
    if stp == "y":
        while stp == "y":
            subreddits_to_poll = []
            subreddit_to_poll = input("What subreddit do you want to poll? Format must be in '/r/<insert subreddit name here>'.")
            subreddits_to_poll.append(subreddit_to_poll)
            stp = input("Do you have more subreddits to poll/track? (y or n)")
    else:
        subreddits_to_poll = ["/r/orangetheory", "/r/NBA", "/r/AskReddit", "/r/NFL", "/r/fitness", "/r/BandofBrothers", "/r/UTAustin"]
    rst = Reddit_scraper_timer(c_id, c_secret, uname, pword, subreddits_to_poll)
    j = 1
    for i in range(26):
        rst.auto_timer(parsing_interval=900, days_delay = j)

if __name__ == '__main__':
    sys.exit(main())