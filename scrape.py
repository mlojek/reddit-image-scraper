import praw
import requests
import os


POST_LIMIT = 100


def lines_from_file(filepath: str) -> list:
    result = []

    with open(filepath, 'r') as input_file:
        for line in input_file.readlines():
            # Get rid of newlines:
            if line[-1] == '\n':
                line = line[0:-1]

            result.append(line)

    return result


def scrape_subreddit_images(reddit, sub_name: str, post_limit: int, sort):
    pass


if __name__ == '__main__':
    client = lines_from_file('client')
    users = lines_from_file('users')
    subreddits = lines_from_file('subreddits')

    # Create a new Reddit instance:
    reddit = praw.Reddit(client_id=client[0],
                         client_secret=client[1],
                         user_agent=client[2])

    for sub in subreddits:
        # Make a subdirectory for the images:
        if sub not in os.listdir('images'):
            os.mkdir(f'images/{sub}')

        # Get the submissions (posts) and save images:
        for submission in reddit.subreddit(sub).hot(limit=POST_LIMIT):
            print(submission.url)

            try:
                extension = submission.url.rsplit('.')[-1]
                file_path = f'images/{sub}/'
                file_name = f'{submission.id}_{submission.author.name}.{extension}'

                # Save to file:
                response = requests.get(submission.url)
                with open(file_path + file_name, "wb") as file:
                    file.write(response.content)
            except FileNotFoundError:
                pass

    for user in users:
        # Make a subdirectory for the images:
        if user not in os.listdir('images'):
            os.mkdir(f'images/{user}')

        for submission in reddit.redditor(user).submissions.hot(limit=1000):
            print(submission.url)

            try:
                extension = submission.url.rsplit('.')[-1]
                file_path = f'images/{user}/'
                file_name = f'{submission.id}_{user}.{extension}'

                # Save to file:
                response = requests.get(submission.url)
                with open(file_path + file_name, "wb") as file:
                    file.write(response.content)
            except FileNotFoundError:
                pass
