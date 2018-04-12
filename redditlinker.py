import discord
import re
import sys

from commands import *

# invite link: http://bit.ly/2lzFAyP

# check if the script is running in debug mode
debug = False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    debug = True

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
    print('Currently in %d servers' % len(client.servers))
    print('------')


@client.event
async def on_message(message):
    # only respond to non-bot messages
    if not message.author.bot:
        text = message.content
        channel = message.channel

        async def send(msg=None, embed=None):
            await client.send_message(channel, msg, embed=embed)

        # initialise
        async def fn(send, *args):
            pass  # do nothing
        args = []
        command_parsed = False
        sub_matches = []

        if text.startswith('/r/') or text.startswith('/R/') or text.startswith('r/') or text.startswith('R/'):
            if text.startswith('/r/') or text.startswith('/R/'):
                args_unparsed = text[3:]
                full_r = True  # flag used later...
            else:
                args_unparsed = text[2:]
                full_r = False

            args_parsed = args_unparsed.split(' ')
            sub = args_parsed[0]

            if len(args_parsed) > 1:
                # if we only have one argument, then the message is just a sub name
                # in that case we need to link to sub, so do nothing in this stage
                error = False
                args.append(sub)
                if args_parsed[1] in ['hot', 'new']:
                    if len(args_parsed) >= 3:
                        # a value for the number of results was supplied
                        try:
                            args.append(int(args_parsed[2]))  # number of results
                        except ValueError:
                            error = True

                    # now pick the appropriate function
                    if args_parsed[1] == 'hot':
                        fn = hot
                    else:
                        fn = new
                else:
                    # TODO: maybe redo the argument order for sub_lookup. Does `results` have to be an optional arg?
                    print(args_parsed)
                    if len(args_parsed) >= 2:
                        # a value for the number of results was supplied, and a query of at least one word
                        args.append(' '.join(args_parsed[2:]))
                        try:
                            args.append(int(args_parsed[1]))  # number of results
                        except ValueError:
                            error = True

                        print(args)

                    fn = sub_lookup

                if not error:
                    command_parsed = True

            # TODO: perhaps it's possible to avoid all this mess and just use a single regex?
            if not command_parsed:
                # no command has fit so far but the message *does* start with a sub name
                # but wait, what if the first word is just '/r/' or 'r/'?
                # can't just check if len <= 3 as that would ignore `r/a` which should be matched
                # we can introduce a flag above:
                if (full_r and len(text) == 3) or (not full_r and len(text) == 2):
                    # do nothing
                    pass
                else:
                    # check if the sub is the entire message
                    first_space = text.find(' ')
                    if first_space == -1:
                        cutoff = len(text)
                    else:
                        cutoff = first_space  # where the sub name ends

                    sub_name = text[:cutoff].split('/')[-1]
                    sub_matches.append(sub_name)

        if not command_parsed:
            # no command has fit so far, so try to just link to sub
            # this regex matches all strings of the form ' /r/abc' but without the '/r/'
            sub_matches += re.findall(r"\s\/?[rR]\/([^\s\/]+)", text)
            if len(sub_matches) > 0:
                # link to sub
                args.append(sub_matches)
                fn = link_subs

        await fn(send, *args)

client.run(login_token)
