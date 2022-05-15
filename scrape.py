import praw
import requests
import os


def lines_from_file(filepath: str) -> list:
    result = []

    with open(filepath, 'r') as input_file:
        for line in input_file.readlines():
            # Get rid of newlines:
            if line[-1] == '\n':
                line = line[0:-1]
            
            result.append(line)
    
    return result


if __name__ == '__main__':
    client = lines_from_file('client')
    users = lines_from_file('users')
    subreddits = lines_from_file('subreddits')

    # Create a new Reddit instance:
    reddit = praw.Reddit(client_id=client[0], client_secret=client[1], user_agent=client[2])

    # # Sav top hottest posts' images from every subreddit:
    for sub in subreddits:
        # Make a subdirectory for the images:
        if not sub in os.listdir('images'):
            os.mkdir(f'images/{sub}')

        for submission in reddit.subreddit(sub).hot(limit=1000):
            print(submission.url)
            
            response = requests.get(submission.url)

            extension = submission.url.rsplit('.')[-1]
            try:
                path = f"images/{sub}/{submission.id}.{extension}"
                print(path)
                with open(path, "wb") as file:
                    file.write(response.content)
            except:
                pass



    for user in users:
        # Make a subdirectory for the images:
        if not user in os.listdir('images'):
            os.mkdir(f'images/{user}')

        for submission in reddit.redditor(user).submissions.hot(limit=1000):
            print(submission.url)
            
            response = requests.get(submission.url)

            extension = submission.url.rsplit('.')[-1]
            try:
                path = f"images/{user}/{submission.id}.{extension}"
                print(path)
                with open(path, "wb") as file:
                    file.write(response.content)
            except:
                pass
