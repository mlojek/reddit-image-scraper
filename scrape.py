import praw
import requests


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

    # Print top hottest posts' title from every subreddit:
    # for sub in subreddits:
    #     hottest_posts = reddit.subreddit(sub).hot(limit=1)
    #     for post in hottest_posts:
    #         print(sub)
    #         print(post.title)

    for submission in reddit.subreddit("polska_wpz").hot(limit=1):
        print(submission.url)
        
        response = requests.get(submission.url)

        extension = submission.url.rsplit('.')[-1]
        with open(f"{submission.id}.{extension}", "wb") as file:
            file.write(response.content)
