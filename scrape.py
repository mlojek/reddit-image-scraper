import praw
import requests
import os


POST_LIMIT = 100
EXTENSIONS = ['png', 'jpg', 'gif', 'jpeg', 'mp4']


def lines_from_file(filepath: str) -> list:
    result = []

    with open(filepath, 'r') as input_file:
        for line in input_file.readlines():
            # Get rid of newlines:
            if line[-1] == '\n':
                line = line[0:-1]

            result.append(line)

    return result


def scrape_subreddit_images(reddit, sub_name: str, post_limit: int) -> None:
    # Create subdirecotry:
    if sub_name not in os.listdir('images'):
        os.mkdir(f'images/{sub_name}')

    for submission in reddit.subreddit(sub_name).hot(limit=post_limit):
        # Check if the media is in a supported format:
        extension = submission.url.rsplit('.')[-1]
        if extension not in EXTENSIONS:
            continue

        # Prepare file path and name:
        author_name = submission.author.name
        file_path = f'images/{sub_name}/'
        file_name = f'{submission.id}_{sub_name}_{author_name}.{extension}'

        # If file already exists, skip
        if file_name in os.listdir(file_path):
            continue

        # Download the image and save it:
        response = requests.get(submission.url)
        with open(file_path + file_name, "wb") as file:
            file.write(response.content)

    # Print prompt:
    print(f'subreddit {sub_name}\t\tDONE')


def scrape_user_images(reddit, user_name: str, post_limit: int) -> None:
    # Create subdirecotry:
    if user_name not in os.listdir('images'):
        os.mkdir(f'images/{user_name}')

    for submission in reddit.redditor(user_name).submissions.hot(limit=post_limit):
        # Check if the media is in a supported format:
        extension = submission.url.rsplit('.')[-1]
        if extension not in EXTENSIONS:
            continue

        # Prepare file path and name:
        sub_name = submission.subreddit.display_name
        file_path = f'images/{user_name}/'
        file_name = f'{submission.id}_{sub_name}_{user_name}.{extension}'

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
    client = lines_from_file('client')
    users = lines_from_file('users')
    subreddits = lines_from_file('subreddits')

    # Create a new Reddit instance:
    reddit = praw.Reddit(client_id=client[0],
                         client_secret=client[1],
                         user_agent=client[2])

    # for sub in subreddits:
    #     scrape_subreddit_images(reddit, sub, 10)

