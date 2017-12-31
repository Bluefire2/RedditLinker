def link_sub(send, sub):
    """
    Sends a link to a reddit sub.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :return: None
    """
    pass


def sub_lookup(send, sub, query, results = 5):
    """
    Looks up the query in the sub's search, and sends the top search results. If sub is 'all' then it searches all of
    reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param query: The search query.
    :param results: The number of search results to send, defaults to 5.
    :return: None
    """
    pass


def top_from_sub(send, sub, type, results = 5):
    """
    Fetches the top results from a subreddit. Can fetch all time/year/6 months/1 month/1 week/1 day. If sub is 'all'
    then it fetches the top results from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param type: The type of "top", for example 'month', 'year', '6month', etc...
    :param results: The number of search results to send, defaults to 5.
    :return: None
    """
    pass


def hot(send, sub, results = 5):
    """
    Fetches the current hot posts from a subreddit. If sub is 'all' then it fetches the hot posts from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param results: the number of posts to send, defaults to 5.
    :return: None
    """
    pass
