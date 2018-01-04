import json
import requests
import asyncio
from urllib.request import Request, urlopen
from discord import Embed

POST_LIMIT = 15
POSTS_AT_A_TIME = 5
MAX_EMBED_TEXT_LENGTH = 100
POST_EMBED_COLOUR = 0x4286f4


# Helper functions:
def embed_posts(source_url, number=5):
    """
    Fetches posts from a Reddit JSON source link, and puts them into embeds. JSON source can be of hot posts, new posts,
    et cetera. For example, to get hot posts from /r/funny, go to https://www.reddit.com/r/funny.json. In general, you
    just append '.json' to the url.

    :param source_url: The JSON source URL.
    :param number: The number of posts to fetch, defaults to 5.
    :return: An array of Embed objects with Reddit posts from the URL.
    """
    req = Request(source_url)
    req.add_header('User-agent', 'Linker')  # do this so that it doesn't get rate-limited and 429ed

    with urlopen(req) as url:
        # parse the JSON into a data object
        data = json.loads(url.read().decode())
        posts = data['data']['children']

        embeds = []

        for i in range(number):
            # parse out the post data
            post = posts[i]['data']
            permalink = 'https://www.reddit.com' + post['permalink']
            url = post['url']
            title = post['title']
            text = post['selftext']

            # use the data to create an embed for this post, and append it to the list of embeds
            embeds.append(embed_post(url, title, text, permalink))

        return embeds


def embed_post(url, title, text, permalink):
    """
    Creates an embed for a reddit post. If the post is an image then the image is embedded directly, otherwise the post
    link or text is embedded.

    :param url: The url that the post links to, can be an empty string if it's a text post.
    :param title: The title of the post.
    :param text: The text of the post, can be an empty string if it's a link post.
    :param permalink: The permalink to the post's comment thread.
    :return: An embed of the post, which can be sent directly to chat.
    """
    # TODO: maybe include the comments permalink for all posts?
    if url != '':
        # it's a link post
        # check if the link is an image or not
        if is_image(url):
            # it's an image post, so embed the image directly
            embed = Embed(title=title,
                          color=POST_EMBED_COLOUR)
            embed.set_image(url=url)
        else:
            # it's a non-image link post, so embed the url as the description
            embed = Embed(title=title,
                          description=url,
                          color=POST_EMBED_COLOUR)
    else:
        # it's a text post, so embed its description (truncate if needed)
        if len(text) > MAX_EMBED_TEXT_LENGTH:
            # text is too long, we need to truncate
            description = text[:MAX_EMBED_TEXT_LENGTH] + '... [(more)](' + permalink + ')'
        else:
            # text is short enough to just embed it completely
            description = text

        embed = Embed(title=title,
                      description=description,
                      color=POST_EMBED_COLOUR)
    return embed


def is_image(url):
    """
    Determines whether a link is an image or not, without downloading it. This function works by only downloading the
    HTTP headers, and checking the content-type.

    :param url: The url to check.
    :return: True if the link is an image, false otherwise.
    """
    try:
        response = requests.head(url)
        c = response.headers.get('content-type')
        if c is None:
            return False  # stops the function from choking on HTTP 3xx, 4xx and 5xx
        else:
            return c[0:5] == 'image'
    except requests.exceptions.MissingSchema:
        return False


async def send_multiple(send, things):
    """
    A "safe-send" function, that can send messages even when they exceed the message limit. It does this by pausing
    between sending enough to satisfy the limit.

    :param send: The sending function. Must only take one parameter. This function will depend on what you want to send.
    :param things: Things to send.
    :return: None
    """
    async def recursive_fn(things_to_send):
        for thing in things_to_send[0:POSTS_AT_A_TIME]:
            await send(thing)

        if len(things_to_send) > 5:
            # execute function again, with a 1000ms delay

            # We do this by using asyncio.ensure_future. A Timer can't take a coroutine as an input, whereas
            # ensure_future does exactly that.
            async def job():
                await asyncio.sleep(1)  # this is where the delay comes in
                await recursive_fn(things_to_send[POSTS_AT_A_TIME:])  # recursive step

            # we launch the job, which includes the delay in it
            asyncio.ensure_future(job())

    await recursive_fn(things[:POST_LIMIT])  # make sure we don't go over the limit


# Command procedures:
async def link_subs(send, subs):
    """
    Send links to a set of Reddit subs.

    :param send: The function to send a message to chat.
    :param subs: The list of the names of subs. Contains at least one element.
    :return: None
    """
    out = '**Subreddits detected**:'
    reddit_base = 'https://www.reddit.com/r/'

    for sub in subs:
        out += '\n' + reddit_base + sub

    await send(out)


async def sub_lookup(send, sub, query, results=5):
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


async def top_from_sub(send, sub, type='all', results=5):
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


async def hot(send, sub, results=5):
    """
    Fetches the current hot posts from a subreddit. If sub is 'all' then it fetches the hot posts from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param results: the number of hot posts to send, defaults to 5.
    :return: None
    """
    source_url = 'https://www.reddit.com/r/' + sub + '.json'
    embeds = embed_posts(source_url, results)
    await send_multiple(lambda e: send(embed=e), embeds)


async def new(send, sub, results=5):
    """
    Fetches the current new posts from a subreddit. If sub is 'all' then it fetches the new posts from all of reddit.

    :param send: The function to send a message to chat.
    :param sub: The name of the sub.
    :param results: the number of posts to send, defaults to 5.
    :return: None
    """
    source_url = 'https://www.reddit.com/r/' + sub + '/new.json'
    embeds = embed_posts(source_url, results)
    await send_multiple(lambda e: send(embed=e), embeds)
