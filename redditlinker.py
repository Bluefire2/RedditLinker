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

        # initialise
        async def fn(send, embed, *args):
            pass  # do nothing
        args = []
        command_parsed = False

        if text.startswith('/r/') or text.startswith('r/'):
            if text.startswith('/r/'):
                args_unparsed = text[3:]
            else:
                args_unparsed = text[2:]

            args_parsed = args_unparsed.split(' ')
            sub = args_parsed[0]

            if len(args_parsed) > 1:
                # if we only have one argument, then the message is just a sub name
                # in that case we need to link to sub, so do nothing in this stage
                error = False
                if args_parsed[1] == 'hot':
                    args.append(sub)

                    if len(args_parsed) >= 3:
                        # a value for the number of results was supplied
                        try:
                            args.append(int(args_parsed[2]))
                        except ValueError:
                            error = True

                    fn = hot

                    if not error:
                        command_parsed = True

        if not command_parsed:
            # no command has fit so far, so try to just link to sub
            # this regex matches all strings of the form '/r/abc' but without the '/r/'
            sub_matches = re.findall(r"/r/([^\s/]+)", text)
            if len(sub_matches) > 0:
                # link to sub
                args.append(sub_matches)
                fn = link_subs

        await fn(send, embed, *args)

client.run(login_token)
