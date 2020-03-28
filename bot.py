import discord
import logging
import time
from configparser import ConfigParser, NoSectionError, NoOptionError
import sys

if __name__ == "__main__":

    client = discord.Client()
    logging.basicConfig(level=logging.INFO, filename='bot_log.log', filemode='w',
                        format='[%(levelname)s] %(asctime)s: %(name)s - %(message)s')

    parser = ConfigParser()
    try:
        with open('bot_config.ini') as config_file:
            parser.read_file(config_file)
    except IOError:
        error_msg = 'No Configuration File found.'
        print(error_msg)
        logging.error(error_msg)
        sys.exit(1)

    @client.event
    async def on_ready():
        login_msg = 'Logged in as {0.user}'.format(client)
        print(login_msg)
        logging.info(login_msg)

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        if message.content.startswith('$repeat'):
            nums = [int(s) for s in message.content.split() if s.isdigit()]
            if nums:
                repeats = nums[0]
                if repeats > 20:
                    await message.channel.send('Maximum 20 repeats allowed.')
                    return
            else:
                repeats = 10
            try:
                user = message.mentions[0]
            except IndexError:
                await message.channel.send('No user mentioned!')
            else:
                for _ in range(repeats):
                    await message.channel.send(user.mention)
                    time.sleep(0.5)

    try:
        token = parser.get('bot_config', 'token')
    except (NoSectionError, NoOptionError):
        error_msg = 'Configuration file not created properly.'
        print(error_msg)
        logging.error(error_msg)
    else:
        client.run(token)
