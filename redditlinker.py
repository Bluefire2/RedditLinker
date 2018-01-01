import discord
import re

from commands import *

debug = True
# invite link: http://bit.ly/2lzFAyP

with open('config.json') as f:
    config = json.load(f)

if debug:
    login_token = config['test_token']
else:
    login_token = config['token']

client = discord.Client()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    # only respond to non-bot messages
    if not message.author.bot:
        text = message.content
        channel = message.channel

        async def send(msg=None, embed=None):
            await client.send_message(channel, msg, embed=embed)

        embed = discord.Embed

        async def fn(send, *args):
            pass  # do nothing

        args = []

        if text.startswith('/r/') or text.startswith('r/'):
            if text.startswith('/r/'):
                args_unparsed = text[3:]
            else:
                args_unparsed = text[2:]

            args_parsed = args_unparsed.split(' ')
            sub = args_parsed[0]

            if args_parsed[1] == 'hot':
                args.append(sub)

                if len(args_parsed) >= 3:
                    # a value for the number of results was supplied
                    try:
                        args.append(int(args_parsed[2]))
                    except ValueError:
                        await send('Error: number of results must be an integer')
                        return

                await hot(send, embed, *args)
        else:
            # this regex matches all strings of the form '/r/abc' but without the '/r/'
            sub_matches = re.findall(r"/r/([^\s/]+)", text)
            if len(sub_matches) > 0:
                # link to sub
                await link_subs(send, embed, sub_matches)

client.run(login_token)
