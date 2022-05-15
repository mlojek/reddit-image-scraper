import praw


if __name__ == '__main__':
    # Get client params:
    client = []
    with open('client', 'r') as client_file:
        for line in client_file.readlines():
            # Get rid of newlines:
            if line[-1] == '\n':
                line = line[0:-1]
            
            client.append(line)

    # Create a new Reddit instance:
    reddit = praw.Reddit(client_id=client[0], client_secret=client[1], user_agent=client[2])

    # Check if it works by scraping top 10 hottest posts' titles:
    hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
    for post in hot_posts:
        print(post.title)
