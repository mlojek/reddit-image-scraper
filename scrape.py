import praw


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

    # Check if it works by scraping top 10 hottest posts' titles:
    hot_posts = reddit.subreddit('MachineLearning').hot(limit=10)
    for post in hot_posts:
        print(post.title)
