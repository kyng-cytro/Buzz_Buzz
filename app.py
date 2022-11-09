import discum
import json
import schedule
import os
from random import randint
import time
from datetime import datetime, timedelta

# TODO: uncomment these if using .env file
from dotenv import load_dotenv

load_dotenv()


def handler(bot):
    data = json.load(open('commands/daily.json'))
    bot.triggerSlashCommand(appID, channelID, guildID, data)
    print("Job completed successfully")


def work(bot):
    # User global variable
    global WORKING
    global LASTRUN

    # Don't Work if one already exists
    if WORKING:
        return

    # Don't Work if it hasn't been an hour since the last
    if (datetime.now() - timedelta(hours=1) < LASTRUN):
        return

    WORKING = True

    # Wait random number of seconds
    wait = randint(600, os.getenv('WAIT'))
    print(f"Wait for {wait} seconds")
    time.sleep(wait)

    # Work
    data = json.load(open('commands/work.json'))
    bot.triggerSlashCommand(appID, channelID, guildID, data)

    # Setup for next work
    LASTRUN = datetime.now()
    WORKING = False

    print("Job completed successfully")


if __name__ == '__main__':
    # Setup
    print("Started....")
    guildID = os.getenv('guildID')
    channelID = os.getenv('channelID')
    appID = os.getenv('appID')
    TOKEN = os.getenv('TOKEN')
    WORKING = False

    # LASTRUN equal to current time minus 1 hour
    LASTRUN = datetime.now() - timedelta(hours=1)

    # Create Self Bot
    bot = discum.Client(token=TOKEN, log=False)

    # Claims Daily
    schedule.every().day.at("21:28").do(
        handler, bot=bot)

    # Work and claim hourly
    schedule.every(1).hour.do(work, bot=bot)

    while True:

        schedule.run_pending()
