import discord
import re
import json

from commands import *

with open('config.json') as f:
    config = json.load(f)

test_token = config['test-token']

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

        async def send(msg):
            await client.send_message(channel, msg)

        sub_matches = re.findall(r"/r/([^\s/]+)", text)
        if len(sub_matches) > 0:
            # link to sub
            await link_subs(send, sub_matches)


client.run(test_token)
