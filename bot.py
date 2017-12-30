import discord
import asyncio
import json

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
    text = message.content
    channel = message.channel

    async def send_fn(msg):
        await client.send_message(channel, msg)


client.run(test_token)
