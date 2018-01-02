import json
from urllib.request import Request, urlopen


def embed_posts(embed, source_url, number=5):
    """
    Fetches posts from a Reddit JSON source link, and puts them into an embed. JSON source can be of hot posts, new
    posts, et cetera. For example, to get hot posts from /r/funny, go to https://www.reddit.com/r/funny.json.

    :param embed: The current embed class.
    :param source_url: The JSON source URL.
    :param number: The number of posts to fetch, defaults to 5.
    :return: An Embed object with Reddit posts from the URL.
    """
    req = Request(source_url)
    req.add_header('User-agent', 'Linker')

    with urlopen(req) as url:
        data = json.loads(url.read().decode())
        posts = data['data']['children']

        e = embed(title=None,
                  description=None,
                  color=0x4286f4)

        for i in range(number):
            post = posts[i]['data']
            permalink = 'https://www.reddit.com' + post['permalink']
            url = post['url']
            title = post['title']
            text = post['selftext']

            if text == '':
                # it's a link post
                field_value = url
            else:
                # it's a text post
                # attach truncated text and a link to the post
                field_value = text[0:100]
                field_value += '... [(more)](' + permalink + ')'

            e.add_field(name=title, value=field_value, inline=False)

        return e


async def link_subs(send, embed, subs):
    """
    Send links to a set of Reddit subs.

    :param send: The function to send a message to chat.
    :param embed: The current embed class.
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
    :param embed: The current embed class.
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
    :param embed: The current embed class.
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
    :param embed: The current embed class.
    :param sub: The name of the sub.
    :param results: the number of hot posts to send, defaults to 5.
    :return: None
    """
    source_url = 'https://www.reddit.com/r/' + sub + '.json'
    e = embed_posts(embed, source_url, results)
    await send(embed=e)


async def new(send, embed, sub, results=5):
    """
    Fetches the current new posts from a subreddit. If sub is 'all' then it fetches the new posts from all of reddit.

    :param send: The function to send a message to chat.
    :param embed: The current embed class.
    :param sub: The name of the sub.
    :param results: the number of posts to send, defaults to 5.
    :return: None
    """
    source_url = 'https://www.reddit.com/r/' + sub + '/new.json'
    e = embed_posts(embed, source_url, results)
    await send(embed=e)
