# Reddit image scraper
Simple and easy to use CLI tool to download images from your favourite reddit communities and users.  

### Client setup
First, you must create a reddit app. This is the guide I followed, which explains it well: https://towardsdatascience.com/scraping-reddit-data-1c0af3040768. Then, save your credentials in `client` file, like this:
```
client_id  
client_secret  
user_agent  
```

### How to use

```
usage: scrape.py [-h] [-r SUBREDDIT] [-R SUBREDDITS_FILE] [-u USER] [-U USERS_FILE]
                 [-s SORT_CRIT] postlimit

Reddit image downloader

positional arguments:
  postlimit             how many posts to process

options:
  -h, --help            show this help message and exit
  -r SUBREDDIT, --subreddit SUBREDDIT
                        subreddit to scrape
  -R SUBREDDITS_FILE, --subreddits-file SUBREDDITS_FILE
                        file containing names of subreddits to scrape
  -u USER, --user USER  user to scrape
  -U USERS_FILE, --users-file USERS_FILE
                        file containing names of users to scrape
  -s SORT_CRIT, --sort-crit SORT_CRIT
                        sorting criterium: hot/top/new/random
```
  
`subreddits_file` and `users_file` should contain desired names, each in a separate line.  

### How images are saved
Only the media of supported extensions are supported: `jpg, jpeg, png, gif, mp4`.  
The media are saved in `images` directory, in a subdirectory named after the subreddit/user it got scraped from.  
The media naming is as follows: `image-name.sub-name.author-name.extension`