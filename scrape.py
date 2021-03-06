import os
import argparse
from enum import IntEnum

import praw
import requests


POST_LIMIT = 100
EXTENSIONS = ['png', 'jpg', 'gif', 'jpeg', 'mp4']


class Sort(IntEnum):
    hot = 0
    new = 1
    top = 2
    random = 3


def lines_from_file(filepath: str) -> list:
    result = []

    with open(filepath, 'r') as input_file:
        for line in input_file.readlines():
            # Get rid of newlines:
            if line[-1] == '\n':
                line = line[0:-1]

            result.append(line)

    return result


def get_subreddit_submissions(reddit, sub_name: str, post_limit: int, sort: int = Sort.hot) -> list:
    if sort == Sort.hot:
        return reddit.subreddit(sub_name).hot(limit=post_limit)
    elif sort == Sort.new:
        return reddit.subreddit(sub_name).new(limit=post_limit)
    elif sort == Sort.top:
        return reddit.subreddit(sub_name).top(limit=post_limit)
    elif sort == Sort.random:
        return [reddit.subreddit(sub_name).random() for _ in range(post_limit)]
    else:
        return reddit.subreddit(sub_name).hot(limit=post_limit)


def scrape_subreddit_images(reddit, sub_name: str, post_limit: int, sort: int = Sort.hot) -> None:
    # Create subdirecotry:
    if sub_name not in os.listdir('images'):
        os.mkdir(f'images/{sub_name}')

    for submission in get_subreddit_submissions(reddit, sub_name, post_limit, sort):
        # Check if the media is in a supported format:
        extension = submission.url.rsplit('.')[-1]
        if extension not in EXTENSIONS:
            continue

        # Prepare file path and name:
        author_name = submission.author.name
        file_path = f'images/{sub_name}/'
        file_name = f'{submission.id}.{sub_name}.{author_name}.{extension}'

        # If file already exists, skip
        if file_name in os.listdir(file_path):
            continue

        # Download the image and save it:
        response = requests.get(submission.url)
        with open(file_path + file_name, "wb") as file:
            file.write(response.content)

    # Print prompt:
    print(f'subreddit {sub_name}\t\tDONE')


def get_user_submissions(reddit, user_name: str, post_limit: int, sort: int = Sort.hot) -> list:
    if sort == Sort.hot:
        return reddit.redditor(user_name).submissions.hot(limit=post_limit)
    elif sort == Sort.new:
        return reddit.redditor(user_name).submissions.new(limit=post_limit)
    elif sort == Sort.top:
        return reddit.redditor(user_name).submissions.top(limit=post_limit)
    else:
        return reddit.redditor(user_name).submissions.hot(limit=post_limit)


def scrape_user_images(reddit, user_name: str, post_limit: int, sort: int = Sort.hot) -> None:
    # Create subdirecotry:
    if user_name not in os.listdir('images'):
        os.mkdir(f'images/{user_name}')

    for submission in get_user_submissions(reddit, user_name, post_limit, sort):
        # Check if the media is in a supported format:
        extension = submission.url.rsplit('.')[-1]
        if extension not in EXTENSIONS:
            continue

        # Prepare file path and name:
        sub_name = submission.subreddit.display_name
        file_path = f'images/{user_name}/'
        file_name = f'{submission.id}.{sub_name}.{user_name}.{extension}'

        # If file already exists, skip
        if file_name in os.listdir(file_path):
            continue

        # Download the image and save it:
        response = requests.get(submission.url)
        with open(file_path + file_name, "wb") as file:
            file.write(response.content)

    # Print prompt:
    print(f'user {user_name}\t\tDONE')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Reddit image downloader")
    parser.add_argument('-r', '--subreddit', type=str, help='subreddit to scrape')
    parser.add_argument('-R', '--subreddits-file', type=str, help='file containing names of subreddits to scrape')
    parser.add_argument('-u', '--user', type=str, help='user to scrape')
    parser.add_argument('-U', '--users-file', type=str, help='file containing names of users to scrape')
    parser.add_argument('-s', '--sort-crit', type=str, help='sorting criterium: hot/top/new/random')
    parser.add_argument('postlimit', type=int, help='how many posts to process')
    args = parser.parse_args()

    # Get client credentials:
    client = lines_from_file('client')

    # Create a new Reddit instance:
    reddit = praw.Reddit(client_id=client[0],
                         client_secret=client[1],
                         user_agent=client[2])

    # Select the sorting criterium:
    sort = Sort.hot
    if args.sort_crit:
        if args.sort_crit == 'new':
            sort = Sort.new
        elif args.sort_crit == 'top':
            sort = Sort.top
        elif args.sort_crit == 'random':
            sort = Sort.random

    # Get to work:
    if args.subreddit:
        scrape_subreddit_images(reddit, args.subreddit, args.postlimit, sort)

    if args.subreddits_file:
        for sub in lines_from_file(args.subreddits_file):
            scrape_subreddit_images(reddit, sub, args.postlimit, sort)

    if args.user:
        scrape_user_images(reddit, args.user, args.postlimit, sort)

    if args.users_file:
        for user in lines_from_file(args.users_file):
            scrape_user_images(reddit, user, args.postlimit, sort)
