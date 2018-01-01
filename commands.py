async def link_subs(send, embed, subs):
    """
    Send links to a set of reddit subs.

    :param send: The function to send a message to chat.
    :param subs: The list of the names of subs. Contains at least one element.
    :return: None
    """
    out = '**Subreddits detected**:'
    reddit_base = 'https://www.reddit.com/r/'

    for sub in subs:
        out += '\n' + reddit_base + sub

    await send(out)


async def sub_lookup(send, embed, sub, query, results = 5):
    """
    Looks up the query in the sub's search, and sends the top search results. If sub is 'all' then it searches all of
    reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param query: The search query.
    :param results: The number of search results to send, embed, async defaults to 5.
    :return: None
    """
    pass


async def top_from_sub(send, embed, sub, type = 'all', results = 5):
    """
    Fetches the top results from a subreddit. Can fetch all time/year/6 months/1 month/1 week/1 day. If sub is 'all'
    then it fetches the top results from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param type: The type of "top", for example 'month', 'year', '6month', etc...
    :param results: The number of search results to send, embed, async defaults to 5.
    :return: None
    """
    pass


async def hot(send, embed, sub, results=5):
    """
    Fetches the current hot posts from a subreddit. If sub is 'all' then it fetches the hot posts from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param results: the number of posts to send, embed, async defaults to 5.
    :return: None
    """
    pass
